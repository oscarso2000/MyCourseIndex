from haystack.nodes import TextConverter, PDFToTextConverter, PreProcessor, FARMReader, TransformersReader, DensePassageRetriever
from haystack.document_stores import FAISSDocumentStore
from haystack.pipelines import ExtractiveQAPipeline, JoinDocuments
from haystack import Pipeline
from haystack.nodes import ElasticsearchRetriever, EmbeddingRetriever
from haystack.utils import launch_es
from haystack.document_stores import ElasticsearchDocumentStore
from pathlib import Path
import json
import re
import convert_pdf_to_string, answer from pipeline
import heapq


'''
Utilizes QA model of Haystack
retriever: retrieve top contexts, uses dense passage retrieval method
reader: does QA, uses roberta
returns the retriever and the whole pipeline
'''
def create_dpr(document_store):
    retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    max_seq_len_query=64,
    max_seq_len_passage=256,
    batch_size=16,
    use_gpu=True,
    embed_title=True,
    use_fast_tokenizers=True,
    )
    document_store.update_embeddings(retriever)
    document_store.save(index_path="haystack_test_faiss", config_path="haystack_test_faiss_config")
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True, progress_bar=False, top_k_per_candidate=2)
    pipe = ExtractiveQAPipeline(reader, retriever)
    return retriever, pipe

'''
ensemble retriever
1 sparse retriever using elastic search
1 dense retriever using embedding retriever
'''
def ensemble_retriever(doc_pdf):
# Initialize DocumentStore and index documents
    launch_es()
    document_store2 = ElasticsearchDocumentStore()
    document_store2.write_documents(doc_pdf)
    es_retriever = ElasticsearchRetriever(document_store=document_store2)

    embedding_retriever = EmbeddingRetriever(
        document_store2,
        model_format="sentence_transformers",
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    )
    document_store2.update_embeddings(embedding_retriever, update_existing_embeddings=False)

    p_ensemble = Pipeline()
    p_ensemble.add_node(component=es_retriever, name="ESRetriever", inputs=["Query"])
    p_ensemble.add_node(component=embedding_retriever, name="EmbeddingRetriever", inputs=["Query"])
    p_ensemble.add_node(
        component=JoinDocuments(join_mode="concatenate"), name="JoinResults", inputs=["ESRetriever", "EmbeddingRetriever"]
    )
    p_ensemble.add_node(component=reader, name="Reader", inputs=["JoinResults"])

    return p_ensemble

'''
retrieve top len_retr passages, produce len_ans number of answers from each passage
return a list containing len_out of (answer, score)
'''
def retriever_reader_pipe(retriever, reader_id, query, len_retr, len_ans, len_out):
    passages = retriever.retrieve(query=query, top_k=len_retr)
    max_score = 0
    pred = []
    for passage in passages:
        for i in range(len_ans):
            ans, score = answer(reader_id, passage, query)
            if len(pred) < len_out:
              heapq.heappush(pred, (ans, score))
            elif score > pred[0][1]:
                heapq.heappushpop(pred, (ans, score))
    return pred


'''
Function that counts number of common words in s0 and s1, 
number of words in s0, and number of words in s1
'''
def common_words(s0, s1):
    s0 = s0.lower()
    s1 = s1.lower()
    s0List = s0.split(" ")
    s1List = s1.split(" ")
    return len(list(set(s0List)&set(s1List))), len(s0List), len(s1List)

'''
Function that returns metrics on the predicted values 
Returns the precision, recall, and f1 score
'''
def evaluate(preds, labels, questions, ids, len_ans):
  n = len(labels)
  precision = 0
  recall = 0
  f1 = 0

  for i in range(n):
    l = labels[i]
    pr, re, f1_c = 0, 0, 0
    for j in range(len_ans):
      p = preds[i][j]
      if len(p) == 0 or len(l) == 0:
        agree = 1 if len(p) == len(l) else 0
        pr = 1
        re = 1
        f1_c = 1
      else:
        intersection, pl, ll = common_words(p,l)
        pr = max((1.0*intersection)/pl, pr)
        re = max((1.0*intersection)/ll, re)

    if pr <= 0.5:
      print("question", questions[i])
      print("label", l)
      print(preds[i])
    precision += pr
    #calculate recall
    recall += re
    #calculate f1
    f1 += 0 if (pr == 0 or re == 0) else (2*pr*re)/(pr+re)

    if (pr == 0 or re == 0):
      print("\nBad answer example ",ids[i], ': ', questions[i])
      print("Prediction: ", p)
      print("Answer: ", l)
      print()

  #average over all samples
  precision = precision/n
  recall = recall/n
  f1 = f1/n

  return precision, recall, f1

def process_json(data_path, imp_toggle):
  question = []
  text = []
  answer = []
  is_impossible = []
  ids = []
  with open(data_path) as f:
    data = json.load(f)["data"]
  
  for d in data:
    if (not d["is_impossible"] or imp_toggle):
      question.append(d["question"])
      text.append(d["context"])
      answer.append(d["answer"])
      is_impossible.append(d["is_impossible"])
      ids.append(d["id"])
  return question, text, answer, is_impossible, ids


def joinParagraph(str):
    s = str.replace('\n', ' ').replace('*', '').replace('%temp%', 'e').replace('```{code-cell} ocaml', '').replace('\ ', '').replace('`', '')
    return re.sub('\\\s',' ', s)

'''
turn files into the documents that can be processed by the Haystack pipeline
store files in document_store
'''
def create_passages(doc_dir, document_store):
    converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
    doc_pdf = converter.convert(file_path=Path(f"{doc_dir}/3110.pdf"), meta=None)[0]
    doc_pdf.content = join_Paragraph(doc_pdf.content)
    # doc_pdf = convert_pdf_to_string(file_path)
    preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="word",
    split_length=100,
    split_respect_sentence_boundary=True,
    )
    docs_default = preprocessor.process(doc_pdf)
    document_store.write_documents(docs_default)
'''
return evaluation of pipe on a data set
'''
def get_evaluation(data_path, len_ans, len_retr, pipe):
  questions, text, labels, _, ids = process_json(data_path, False)
  preds = []
  for q in questions:
    prediction = pipe.run(
    query=q, params={"Retriever": {"top_k": len_retr}, "Reader": {"top_k": len_ans}})
    ans = [prediction['answers'][i].answer for i in range(len_ans)]
    preds.append(ans)

  p, r, f1 = evaluate(preds, labels, questions, ids, len_ans)
  return p, r, f1

if __name__ == '__main__':
    document_store = FAISSDocumentStore(faiss_index_factory_str="Flat", sql_url= "sqlite:///haystack_test_faiss.db")
    document_store = document_store.load(index_path="haystack_test_faiss", config_path="haystack_test_faiss_config")
	  create_passages(doc_dir, document_store)
    retriever, pipe = create_dpr(document_store)

    len_ans = 5
    len_retr = 10

    p, r, f1 = get_evaluation(data_path, len_ans, len_retr, pipe)
    print(p, r, f1)
