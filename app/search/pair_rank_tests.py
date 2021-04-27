from scipy.optimize import minimize
import itertools
import numpy as np
import networkx as nx
import random
from numpy.linalg import multi_dot
import datetime
import math
import sys
import os

import time
from tqdm import tqdm

import datasets
import torch
import numpy as np
from transformers import AutoModel, AutoModelForSeq2SeqLM, AutoTokenizer


class LinearModel:
    def __init__(self, n_features, learning_rate, n_candidates=0, learning_rate_decay=1.0):
        self.n_features = n_features
        self.learning_rate = learning_rate
        self.n_models = n_candidates + 1
        self.weights = np.zeros((n_features, self.n_models))
        self.learning_rate_decay = learning_rate_decay

    def copy(self):
        copy = LinearModel(n_features=self.n_features, learning_rate=self.learning_rate, n_candidates=self.n_models - 1)
        copy.weights = self.weights.copy()
        return copy

    def candidate_score(self, features):
        self._last_features = features
        return np.dot(features, self.weights).T

    def score(self, features):
        self._last_features = features
        return np.dot(features, self.weights[:, 0:1])[:, 0]

    def update_weights(self, weights):
        self.weights[:, 0] = weights

    def update_to_gradient_inner_loop(self, gradient):
        self.weights[:, 0] += self.learning_rate * gradient

    def update_to_gradient(self, gradient):
        self.weights[:, 0] += self.learning_rate * gradient
        self.learning_rate *= self.learning_rate_decay


# Pairwise Logistic Regression
def logist(s):
    return 1 / (1 + np.exp(-s))


def logistic_func(theta, x):
    return float(1) / (1 + math.e ** (-x.dot(theta)))


def safe_ln(x, minval=0.0000000001):
    return np.log(x.clip(min=minval))


def update_edges(super_edges, candidate_nodes, new_id):
    # create new edges for the new node
    new_edges = set()
    for i in candidate_nodes:
        new_edges = new_edges.union(super_edges[i])
    new_edges.remove(new_id)
    super_edges[new_id] = new_edges
    # remove the merged nodes
    for i in candidate_nodes:
        if i != new_id:
            super_edges.pop(i)
    # update the edges in other nodes
    for i in super_edges.keys():
        if super_edges[i] & candidate_nodes:
            for n in candidate_nodes:
                try:
                    super_edges[i].remove(n)
                except Exception as e:
                    print(e)
                    pass
            if i != new_id:
                super_edges[i].add(new_id)
    return super_edges


def update_nodes(super_nodes, candidate_nodes, new_id):
    new_node = set()
    for i in candidate_nodes:
        new_node = new_node.union(set(super_nodes[i]))
    super_nodes[new_id] = new_node
    for i in candidate_nodes:
        if i != new_id:
            super_nodes[i] = {}
    return super_nodes

class PairRank: #(BasicOnlineRanker):
    def __init__(self, alpha, _lambda, refine, rank, update, learning_rate, learning_rate_decay, ind, n_results, n_features):
        # super(PairRank, self).__init__(*args, **kargs)

        self.n_features = n_features
        self.n_results = n_results

        self.n_interactions = 0
        self.model_updates = 0
        self._messages = {}
        self._default_messages = {}

        self.alpha = alpha
        self._lambda = _lambda
        self.refine = refine
        self.rank = rank
        self.update = update
        self.learning_rate = learning_rate
        self.learning_rate_decay = learning_rate_decay
        self.ind = ind
        self.A = self._lambda * np.identity(self.n_features)
        self.InvA = np.linalg.pinv(self.A)
        self.model = LinearModel(
            n_features=self.n_features, learning_rate=learning_rate, learning_rate_decay=1, n_candidates=1,
        )
        self.history = {}
        self.n_pairs = []
        self.pair_index = []
        self.log = {}
        self.get_name()

    @staticmethod
    def default_parameters():
        parent_parameters = BasicOnlineRanker.default_parameters()
        parent_parameters.update({"learning_rate": 0.1, "learning_rate_decay": 1.0})
        return parent_parameters

    def get_test_rankings(self, features):
        scores = -self.model.score(features)
        ordering = scores.argsort(axis=scores.ndim-1)
        return ordering[..., self.n_results:]

    def cost_func_reg(self, theta, x, y):
        log_func_v = logistic_func(theta, x)
        step1 = y * safe_ln(log_func_v)
        step2 = (1 - y) * safe_ln(1 - log_func_v)
        final = (-step1 - step2).mean()
        final += self._lambda * theta.dot(theta)
        return final

    def log_gradient_reg(self, theta, x, y):
        # n = len(y)
        first_calc = logistic_func(theta, x) - y
        final_calc = first_calc.T.dot(x) / len(y)
        reg = 2 * self._lambda * theta
        final_calc += reg
        return final_calc

    def get_name(self):
        if self.update == "gd" or self.update == "gd_diag" or self.update == "gd_recent":
            self.name = "PAIRRANK-None-None-{}-{}-{}-{}-{}-{}".format(
                self.update, self._lambda, self.alpha, self.refine, self.rank, self.ind
            )
        else:
            self.name = "PAIRRANK-{}-{}-{}-{}-{}-{}-{}-{}".format(
                self.learning_rate,
                self.learning_rate_decay,
                self.update,
                self._lambda,
                self.alpha,
                self.refine,
                self.rank,
                self.ind,
            )

    def get_lcb(self, query_feat):

        if self.update == "gd_diag":
            # InvA = np.diag(np.diag(self.InvA))
            Id = np.identity(self.InvA.shape[0])
            InvA = np.multiply(self.InvA, Id)
        else:
            InvA = self.InvA

        pairwise_feat = (query_feat[:, np.newaxis] - query_feat).reshape(-1, self.n_features)
        pairwise_estimation = self.model.score(pairwise_feat)
        n_doc = len(query_feat)
        prob_est = logist(pairwise_estimation).reshape(n_doc, n_doc)
        for i in range(n_doc):
            for j in range(i + 1, n_doc):
                feat = query_feat[i] - query_feat[j]
                uncertainty = self.alpha * np.sqrt(np.dot(np.dot(feat, InvA), feat.T))
                prob_est[i, j] -= uncertainty
                prob_est[j, i] -= uncertainty
        lcb_matrix = prob_est

        return lcb_matrix

    def get_partitions(self, lcb_matrix):
        n_nodes = len(lcb_matrix)
        # find all the certain edges
        certain_edges = set()
        for i in range(n_nodes):
            indices = [k for k, v in enumerate(lcb_matrix[i]) if v > 0.5]
            for j in indices:
                certain_edges.add((i, j))

        # refine the certain edges: remove the cycles between partitions.
        if self.refine:
            nodes = np.array(range(n_nodes))
            certainG = nx.DiGraph()
            certainG.add_nodes_from(nodes)
            certainG.add_edges_from(certain_edges)

            for n in certainG.nodes():
                a = nx.algorithms.dag.ancestors(certainG, n)
                for k in a:
                    certain_edges.add((k, n))

        # cut the complete graph by the certain edges
        uncertainG = nx.complete_graph(n_nodes)
        uncertainG.remove_edges_from(certain_edges)
        # get all the connected component by the uncertain edges
        sn_list = list(nx.connected_components(uncertainG))
        n_sn = len(sn_list)
        super_nodes = {}
        for i in range(n_sn):
            super_nodes[i] = sn_list[i]
        # create inv_cp to store the cp_id for each node
        inv_sn = {}
        for i in range(n_sn):
            for j in super_nodes[i]:
                inv_sn[j] = i
        super_edges = {}
        for i in range(n_sn):
            super_edges[i] = set([])
        for i, e in enumerate(certain_edges):
            start_node, end_node = e[0], e[1]
            start_sn, end_sn = inv_sn[start_node], inv_sn[end_node]
            if start_sn != end_sn:
                super_edges[start_sn].add(end_sn)

        SG = nx.DiGraph(super_edges)
        flag = True
        cycle = []
        try:
            cycle = nx.find_cycle(SG)
        except Exception as e:
            flag = False

        while flag:
            # get all candidate nodes
            candidate_nodes = set()
            for c in cycle:
                n1, n2 = c
                candidate_nodes.add(n1)
                candidate_nodes.add(n2)
            new_id = min(candidate_nodes)
            # update the edges
            super_edges = update_edges(super_edges, candidate_nodes, new_id)
            super_nodes = update_nodes(super_nodes, candidate_nodes, new_id)
            # print("=======After merge {}=======".format(cycle))
            # print("super_edges: ", super_edges)
            # print("super_nodes: ", super_nodes)

            SG = nx.DiGraph(super_edges)
            try:
                cycle = nx.find_cycle(SG)
            except Exception as e:
                print(e)
                flag = False

        sorted_list = list(nx.topological_sort(SG))

        # self.log[self.n_interactions]["partition"] = super_nodes
        # self.log[self.n_interactions]["sorted_list"] = sorted_list
        return super_nodes, sorted_list

    def _create_train_ranking(self, query_feat):
        # record the information
        # self.log[self.n_interactions] = {}
        # self.log[self.n_interactions]["qid"] = query_id

        # t1 = datetime.datetime.now()
        lcb_matrix = self.get_lcb(query_feat)
        # t2 = datetime.datetime.now()
        partition, sorted_list = self.get_partitions(lcb_matrix)
        # t3 = datetime.datetime.now()
        ranked_list = []

        for i, k in enumerate(sorted_list):
            cur_p = list(partition[k])

            if self.rank == "random":
                np.random.shuffle(cur_p)
            elif self.rank == "mean":
                feat = query_feat[cur_p]
                score = self.model.score(feat)
                ranked_idx = np.argsort(-score)
                ranked_id = np.array(cur_p)[ranked_idx]
                cur_p = ranked_id.tolist()
            elif self.rank == "certain":
                parent = {}
                child = {}
                for m in cur_p:
                    for n in cur_p:
                        if lcb_matrix[m][n] > 0.5:
                            if m not in child.keys():
                                child[m] = [n]
                            else:
                                child[m].append(n)
                            if n not in parent.keys():
                                parent[n] = [m]
                            else:
                                parent[n].append(m)
                # topological sort
                candidate = []
                for m in cur_p:
                    if m not in parent.keys():
                        candidate.append(m)

                ranked_id = []
                while len(candidate) != 0:
                    node = np.random.choice(candidate)
                    ranked_id.append(node)
                    candidate.remove(node)
                    if node in child.keys():
                        children = child[node]
                    else:
                        children = []
                    for j in children:
                        parent[j].remove(node)
                        if len(parent[j]) == 0:
                            candidate.append(j)
                cur_p = ranked_id
            else:
                print("Rank method is incorrect")
                sys.exit()

            ranked_list.extend(cur_p)

        self.ranking = np.array(ranked_list)
        self._last_query_feat = query_feat
        # self.log[self.n_interactions]["ranking"] = self.ranking
        # self.log[self.n_interactions]["model"] = self.model.weights[:, 0]

        return np.array(ranked_list)

    def update_to_interaction(self, clicks):
        if np.any(clicks):
            self._update_to_clicks(clicks)

    def generate_pairs(self, clicks):
        n_docs = self.ranking.shape[0]
        cur_k = np.minimum(n_docs, self.n_results)
        included = np.ones(cur_k, dtype=np.int32)
        if not clicks[-1]:
            included[1:] = np.cumsum(clicks[::-1])[:0:-1]
        neg_ind = np.where(np.logical_xor(clicks, included))[0]
        pos_ind = np.where(clicks)[0]

        pos_r_ind = self.ranking[pos_ind]
        neg_r_ind = self.ranking[neg_ind]

        if self.ind:
            np.random.shuffle(pos_r_ind)
            np.random.shuffle(neg_r_ind)
            pairs = list(zip(pos_r_ind, neg_r_ind))
        else:
            pairs = list(itertools.product(pos_r_ind, neg_r_ind))

        for p in pairs:
            diff_feat = (self._last_query_feat[p[0]] - self._last_query_feat[p[1]]).reshape(1, -1)
            self.InvA -= multi_dot([self.InvA, diff_feat.T, diff_feat, self.InvA]) / float(
                1 + np.dot(np.dot(diff_feat, self.InvA), diff_feat.T)
            )

        return pairs

    def update_history(self, pairs, last_feat):
        # query_id = self._last_query_id
        idx = len(self.history)
        self.history[idx] = {}
        # self.history[idx]["qid"] = query_id
        self.history[idx]["pairs"] = pairs
        self.history[idx]["feat"] = last_feat

    def generate_training_data(self):
        train_x = []
        train_y = []

        if self.update == "gd_recent":
            # only use the most recent observations to update the model
            max_ind = max(self.history.keys())
            for idx in range(max(max_ind - 500, 0), max_ind + 1):
                # qid = self.history[idx]["qid"]
                # feat = self.get_query_features(qid, self._train_features, self._train_query_ranges)
                pairs = self.history[idx]["pairs"]
                pos_ids = [pair[0] for pair in pairs]
                neg_ids = [pair[1] for pair in pairs]
                x = feat[pos_ids] - feat[neg_ids]
                train_x.append(x)

                y = np.ones(len(pairs))
                train_y.append(y)
        else:
            for idx in self.history.keys():
                # qid = self.history[idx]["qid"]
                # feat = self.get_query_features(qid, self._train_features, self._train_query_ranges)
                feat = self.history[idx]['feat']
                pairs = self.history[idx]["pairs"]
                pos_ids = [pair[0] for pair in pairs]
                neg_ids = [pair[1] for pair in pairs]
                x = feat[pos_ids] - feat[neg_ids]
                train_x.append(x)

                y = np.ones(len(pairs))
                train_y.append(y)

        train_x = np.vstack(train_x)
        train_y = np.hstack(train_y)

        return train_x, train_y

    def process_clicks(self, clicks):
        self.update_to_interaction(clicks)
        self.n_interactions += 1

    def _update_to_clicks(self, clicks):

        # generate all pairs from the clicks
        pairs = self.generate_pairs(clicks)
        n_pairs = len(pairs)
        if n_pairs == 0:
            return
        pairs = np.array(pairs)
        self.update_history(pairs, self._last_query_feat)
        self.n_pairs.append(n_pairs)
        if len(self.n_pairs) == 1:
            self.pair_index.append(n_pairs)
        else:
            self.pair_index.append(self.pair_index[-1] + n_pairs)

        if self.update == "gd" or self.update == "gd_diag" or self.update == "gd_recent":
            self.update_to_history()
        elif self.update == "sgd":
            self.update_sgd(pairs)
        elif self.update == "batch_sgd":
            self.update_batch_sgd()
        else:
            print("Wrong update mode")

    def update_batch_sgd(self):
        n_sample = self.pair_index[-1]
        batch_size = min(n_sample, 128)
        batch_index = random.sample(range(n_sample), batch_size)

        data_id = []
        data_index = []
        for i in batch_index:
            j = 0
            while self.pair_index[j] <= i:
                j += 1
            if j == 0:
                start = 0
            else:
                start = self.pair_index[j - 1]
            data_id.append(j)
            data_index.append(i - start)
        # generate training data
        batch_x = []
        batch_y = []
        for i in range(batch_size):
            # print i, data_id[i]
            idx = data_id[i]
            qid = self.history[idx]["qid"]
            feat = self.get_query_features(qid, self._train_features, self._train_query_ranges)
            pairs = self.history[idx]["pairs"][data_index[i]]
            feat = feat[pairs[0]] - feat[pairs[1]]
            batch_x.append(feat)
            batch_y.append(1)

        batch_x = np.array(batch_x).reshape(-1, self.n_features)
        batch_y = np.array(batch_y).reshape(-1, 1)

        gradient = self.log_gradient_reg(self.model.weights[:, 0], batch_x, batch_y)
        self.model.update_to_gradient(-gradient)

    def update_sgd(self, pairs):

        feat = self.get_query_features(self._last_query_id, self._train_features, self._train_query_ranges)
        n_p = pairs.shape[0]
        pos_feat = feat[pairs[:, 0]] - feat[pairs[:, 1]]
        pos_label = np.ones(n_p)

        gradient = self.log_gradient_reg(self.model.weights[:, 0], pos_feat, pos_label)
        self.model.update_to_gradient(-gradient)

    def update_to_history(self):
        train_x, train_y = self.generate_training_data()
        myargs = (train_x, train_y)
        betas = np.random.rand(train_x.shape[1])
        result = minimize(
            self.cost_func_reg,
            x0=betas,
            args=myargs,
            method="L-BFGS-B",
            jac=self.log_gradient_reg,
            options={"ftol": 1e-6},
        )
        self.model.update_weights(result.x)


class FeatureGenerator:
    
    def __init__(self, n_features):
        self.n_features = n_features
    
    def get_query_features(self, queries, documents):
        features = []
        # for q in queries:
        np.random.seed(queries)
        for _ in documents:
            temp_q = np.random.random((self.n_features,))
            features.append(temp_q)
        
        return np.array(features)

class RetriFeatureGenerator:
    
    def __init__(self, n_features, qar_tokenizer, qar_model, documents):
        self.n_features = 256
        self.qar_tokenizer = qar_tokenizer
        self.qar_model = qar_model
        
        doc_features = []
        with torch.no_grad():
            for d in tqdm(documents):
                a_toks = qar_tokenizer.batch_encode_plus([d], padding=True, max_length=512, truncation=True)
                a_ids, a_mask = (
                    torch.LongTensor(a_toks["input_ids"]),
                    torch.LongTensor(a_toks["attention_mask"]),
                )

                a_reps = qar_model.embed_answers(a_ids, a_mask).type(torch.float32).numpy()
                a_reps = (a_reps / np.linalg.norm(a_reps, axis=1)[:, None])
                
                doc_features.append(a_reps)
        
        self.doc_features = np.array(doc_features)
    
    def get_query_features(self, queries, documents):
        features = []
        
        doc_features = []
        with torch.no_grad():
            q_toks = qar_tokenizer.batch_encode_plus([queries], padding=True, max_length=512, truncation=True)
            q_ids, q_mask = (
                torch.LongTensor(q_toks['input_ids']),
                torch.LongTensor(q_toks['attention_mask']),
            )
            
            q_reps = qar_model.embed_questions(q_ids, q_mask).numpy()
            q_reps = (q_reps / np.linalg.norm(q_reps, axis=1)[:, None])
            
            # features = [np.concatenate([q_reps.flatten(), a_rep.flatten(), np.dot(q_reps, a_rep.T).flatten()]).flatten() for a_rep in self.doc_features]
            features = [np.concatenate([np.dot(q_reps, a_rep.T).flatten(), np.ones((1,1)).flatten()]).flatten() for a_rep in self.doc_features]
        
        return np.array(features)


class Simulate:

    def __init__(self, featuregenerator, n_impressions):
        self.featuregenerator = featuregenerator
        self.n_impressions = n_impressions
    
    def sample_and_rank(self, ranker, queries, documents):
        query_feat = self.featuregenerator.get_query_features(queries, documents)
        ranking_i = ranker._create_train_ranking(query_feat)
        
        return ranking_i
    
    def evaluate_ranking(self, ranker, query, documents, labels):
        dcg = 0
        
        for q, l in zip(query, labels):
            features = self.featuregenerator.get_query_features(q, documents)
            ranking = ranker.get_test_rankings(features)
            for i, rel in enumerate(l[ranking]):
                dcg += rel / np.log2(i+2)
            
        return dcg
        
    
    def run(self, ranker, sample_queries, documents, sample_labels):
        start_time = time.time()
        
        run_results = []
        impressions = 0
        
        n_queries = len(sample_queries)
        
        idx_d = np.random.randint(0, len(documents), size=(100,)) 
        test_queries = sample_queries[idx_d] #np.array([1000001, 1000002, 1000003, 1000004, 1000005])
        test_documents = documents #np.arange(100)
        test_labels = sample_labels[idx_d] # np.array([np.random.binomial(n=1, p=0.15, size=(100,)) for _ in test_queries])
        
        # max_dcg = sum([1/(np.log2(i+2)) for i in range(int(test_labels.sum()))])
        max_dcg = sum([sum([1/(np.log2(i+2)) for i in range(int(l.sum()))]) for l in test_labels])
        
        print(f"Num relevant across all samples: {test_labels.sum()}")
        print(f"Max DCG: {max_dcg}")
        
        dcg_vals = []
        
        for _ in tqdm(range(self.n_impressions), desc="Impressions"):
            test_dcg = self.evaluate_ranking(ranker, test_queries, test_documents, test_labels)
            dcg_vals.append(test_dcg)
            # print(f"DCG: {test_dcg}")
            
            
            impressions = np.random.randint(0, n_queries)
            
            sample_clk_temp = sample_labels[impressions]
            sample_clk_temp = np.random.choice(sample_clk_temp, size=(max(int(0.5*len(sample_clk_temp)), 1),))
            sample_clicks = np.array([1 if i in sample_clk_temp else 0 for i in range(10)])
            
            ranking_i = self.sample_and_rank(
                ranker,
                sample_queries[impressions],
                documents
            )
            
            ranker.process_clicks(sample_clicks)
        
        test_dcg = self.evaluate_ranking(ranker, test_queries, test_documents, test_labels)
        dcg_vals.append(test_dcg)
        # print(f"DCG: {test_dcg}")
        
        return dcg_vals, max_dcg


if __name__ == '__main__':
    eli5 = datasets.load_dataset("eli5")

    qar_tokenizer = AutoTokenizer.from_pretrained('yjernite/retribert-base-uncased')
    qar_model = AutoModel.from_pretrained('yjernite/retribert-base-uncased')

    n_items = 4000 # 10000

    documents = [x['text'][0] for x in eli5['train_eli5']['answers'][:n_items]]

    with torch.no_grad():
        doc_arrays = []
        for d in tqdm(documents):
            a_toks = qar_tokenizer.batch_encode_plus([d], padding=True, truncation=True, max_length=512)
            a_ids, a_mask = (
                torch.LongTensor(a_toks["input_ids"]),
                torch.LongTensor(a_toks["attention_mask"]),
            )

            a_reps = qar_model.embed_answers(a_ids, a_mask).type(torch.float32).numpy()
            a_reps = (a_reps / np.linalg.norm(a_reps, axis=1)[:, None])

            doc_arrays.append(a_reps)

        doc_arrays = np.array(doc_arrays)


    sample_queries = np.array(eli5['train_eli5']['title'][:n_items])

    query_arrays = []
    with torch.no_grad():
        for q in tqdm(sample_queries):
            q_toks = qar_tokenizer.batch_encode_plus([q], padding=True, truncation=True, max_length=512)
            q_ids, q_mask = (
                torch.LongTensor(q_toks["input_ids"]),
                torch.LongTensor(q_toks["attention_mask"]),
            )

            q_reps = qar_model.embed_questions(q_ids, q_mask).type(torch.float32).numpy()
            q_reps = (q_reps / np.linalg.norm(q_reps, axis=1)[:, None])

            query_arrays.append(q_reps.flatten())

        query_arrays = np.array(query_arrays)


    query_arrays = query_arrays.reshape((-1, 128))
    doc_arrays = doc_arrays.reshape((-1, 128))

    sample_labels = np.dot(doc_arrays, query_arrays.T) # np.eye(n_items)

    sample_labels = (sample_labels > 0.33).astype(np.float32)# .sum(axis=1)

    feat_gen = RetriFeatureGenerator(256, qar_tokenizer, qar_model, documents) #FeatureGenerator(100)
    sim = Simulate(feat_gen, 10000)

    ranker = PairRank(0.1, 0.1, True, 'random', 'gd', 0.1, 1, True, 10, 2)# 257)

    dcg_vals, max_dcg = sim.run(ranker, sample_queries, documents, sample_labels)

    import json

    with open("pair_rank_test_res.json", "w") as fp:
        json.dump({"max_dcg": max_dcg, "dcg_vals": [float(x) for x in dcg_vals]}, fp, indent=2)
