""" SimString implementation in Python to extend the C++ version. We created
our own in addition to pip install the reference implementation b/c the
reference implementation is used by the concept mapper however this is useful
to test for boolean like searches where misspellings may occur so that we may
instantly find the relevant results.

Note: Theorhetically one could generate a string that is nonsensical and
is considered a match by having enough ngrams line up

Reference implementation: https://github.com/chokkan/simstring
Paper for all equations: https://dl.acm.org/doi/pdf/10.5555/1873781.1873877
"""
from collections import defaultdict
from operator import itemgetter
from typing import List, Tuple

from multiset import Multiset
from numpy import sqrt, ceil, floor

############################## Feature Extractor ##############################
class CharNgramFeatureExtractor(object):
    """CharNgramFeatureExtractor generates features of a given size for any s.

    .. note::
        This class is simply a nice wrapper but we could simply directly
        modify the 'database'

    :param n: number of elements to extract from a contiguous sequence
    :type n: int
    """
    def __init__(self, n=3):
        self.n = n
    
    def _ngram(self, s: str, n: int) -> List[str]:
        """_each_ngram generates ngrams for the features of a string

        :param s: string to generate ngrams for
        :type s: str
        :param n: number of elements to extract from a contiguous sequence
        :type n: int
        :return: List of ngrams
        :rtype: List[str]
        """
        return [s[i:i+n] for i in range(len(s)-n+1)]
    
    def features(self, string: str) -> List[str]:
        """features generates ngrams for a string.

        :param string: string to generate ngrams for
        :type string: str
        :return: List of ngrams
        :rtype: List[str]
        """
        return self._ngram(" " + string + " ", self.n)
############################# Similarity Measures #############################
# Use the table 1 to get min_feature, max_feature, and tau (min intersect)
# Eq. 3 + 4 also contain equations to constrain the search field which
# is critical to ensuring efficiency
class BaseSimilarity(object):
    """BaseSimilarity is used as a superclass to all similarity measures."""

    def min_Y(self, x_size: int, alpha: float) -> int:
        """min_Y returns the minimum feature set size according to the paper.

        :param x_size: feature size of the input query
        :type x_size: int
        :param alpha: Similarity Threshold
        :type alpha: float
        :raises NotImplementedError: The functions are not implemented since
            this is a base level class
        :return: minimum search range for possible strings Y
        :rtype: int
        """
        raise NotImplementedError

    def max_Y(self, x_size: int, alpha: float) -> int:
        """max_Y returns the maximum feature set size according to the paper.

        :param x_size: feature size of the input query
        :type x_size: int
        :param alpha: Similarity Threshold
        :type alpha: float
        :raises NotImplementedError: The functions are not implemented since
            this is a base level class
        :return: maximum search range for possible strings Y
        :rtype: int
        """
        raise NotImplementedError

    def tau(self, x_size: int, y_size: int, alpha: float) -> int:
        """tau returns the minimum features in common between X and Y.

        :param x_size: feature size of the input query
        :type x_size: int
        :param y_size: feature size 
        :type y_size: int
        :param alpha: Similarity threshold
        :type alpha: float
        :raises NotImplementedError: The functions are not implemented since
            this is a base level class
        :return: minimum features in common needed
        :rtype: int
        """
        raise NotImplementedError

    def similarity(self, X: List[str], Y: List[str]) -> float:
        """similarity returns the measured similarity between the features.

        :param X: features extracted from the query
        :type X: List[str]
        :param Y: features extracted from the canidate string
        :type Y: List[str]
        :raises NotImplementedError: The functions are not implemented since
            this is a base level class
        :return: The measured similarity between 0 and 1
        :rtype: float
        """
        raise NotImplementedError

class CosineSimilarity(BaseSimilarity):
    """CosineSimilarity represents the cosine similarity measure."""

    def min_Y(self, x_size: int, alpha: float) -> int:
        """min_Y returns the minimum feature set size according to the paper.

        :param x_size: feature size of the input query
        :type x_size: int
        :param alpha: Similarity Threshold
        :type alpha: float
        :return: minimum search range for possible strings Y
        :rtype: int
        """
        return int(ceil( (alpha**2) * x_size ))

    def max_Y(self, x_size: int, alpha: float) -> int:
        """max_Y returns the maximum feature set size according to the paper.

        :param x_size: feature size of the input query
        :type x_size: int
        :param alpha: Similarity Threshold
        :type alpha: float
        :return: maximum search range for possible strings Y
        :rtype: int
        """
        return int(floor( float(x_size) / (alpha**2) ))

    def tau(self, x_size: int, y_size: int, alpha: float) -> int:
        """tau returns the minimum features in common between X and Y.

        :param x_size: feature size of the input query
        :type x_size: int
        :param y_size: feature size 
        :type y_size: int
        :param alpha: Similarity threshold
        :type alpha: float
        :return: minimum features in common needed
        :rtype: int
        """
        return int(ceil( alpha * sqrt(x_size * y_size) ))

    def similarity(self, X: List[str], Y: List[str]) -> float:
        """similarity returns the measured similarity between the features.

        :param X: features extracted from the query
        :type X: List[str]
        :param Y: features extracted from the canidate string
        :type Y: List[str]
        :raises NotImplementedError: The functions are not implemented since
            this is a base level class
        :return: The measured similarity between 0 and 1
        :rtype: float
        """
        return float(len(Multiset(X) & Multiset(Y))) / sqrt( len(Multiset(X)) * len(Multiset(Y)) )


class JaccardSimilarity(BaseSimilarity):
    """JaccardSimilarity represents the cosine similarity measure."""

    def min_Y(self, x_size: int, alpha: float) -> int:
        """min_Y returns the minimum feature set size according to the paper.

        :param x_size: feature size of the input query
        :type x_size: int
        :param alpha: Similarity Threshold
        :type alpha: float
        :return: minimum search range for possible strings Y
        :rtype: int
        """
        return int(ceil( alpha * x_size ))

    def max_Y(self, x_size: int, alpha: float) -> int:
        """max_Y returns the maximum feature set size according to the paper.

        :param x_size: feature size of the input query
        :type x_size: int
        :param alpha: Similarity Threshold
        :type alpha: float
        :return: maximum search range for possible strings Y
        :rtype: int
        """
        return int(floor( float(x_size) / alpha ))

    def tau(self, x_size: int, y_size: int, alpha: float) -> int:
        """tau returns the minimum features in common between X and Y.

        :param x_size: feature size of the input query
        :type x_size: int
        :param y_size: feature size 
        :type y_size: int
        :param alpha: Similarity threshold
        :type alpha: float
        :return: minimum features in common needed
        :rtype: int
        """
        return int(ceil( (alpha * (x_size + y_size)) / (1 + alpha) ))

    def similarity(self, X: List[str], Y: List[str]) -> float:
        """similarity returns the measured similarity between the features.

        :param X: features extracted from the query
        :type X: List[str]
        :param Y: features extracted from the canidate string
        :type Y: List[str]
        :raises NotImplementedError: The functions are not implemented since
            this is a base level class
        :return: The measured similarity between 0 and 1
        :rtype: float
        """
        return float(len(Multiset(X) & Multiset(Y))) / sqrt( len(Multiset(X) | Multiset(Y)) )

################################## Databases ##################################
def defaultdict_multiset() -> defaultdict:
    """defaultdict_multiset is a wrapper b/c errors....

    Reference Line 198 within the code for why.

    :return: defaultdict with Multiset as default value
    :rtype: defaultdict[Multiset]
    """
    return defaultdict(Multiset)

class RamDatabase(object):
    """RamDatabase [summary]

    :param feature_extractor: [description]
    :type feature_extractor: :class:`~CharNgramFeatureExtractor`

    .. note::
        We currently force the use of the :class:`~CharNgramFeatureExtractor`
        although we could either extend to other features OR directly integrate
        into the DB.

    .. todo::
        Determine whether to keep feature extractor separate
    """
    def __init__(self, feature_extractor: CharNgramFeatureExtractor):
        self.feature_extractor = feature_extractor
        self.strings = []
        self.locations = []
        self.feature_set_size_to_string_map = defaultdict(Multiset)
        # Just wrapping in lambda to prevent TypeError: first argument must
        # be callable or None. Python has weird things.....
        # Have to extract from the lambda to allow pickling
        self.feature_set_size_and_feature_to_string_map = defaultdict(defaultdict_multiset)

    def add(self, string: str, location: str) -> None:
        """add inserts the string and location into our DB for quick access.

        :param string: string to insert into our database
        :type string: str
        :param location: document in which the string is stored
        :type location: str
        """
        features = self.feature_extractor.features(string)
        size = len(features)

        self.strings.append(string)
        self.locations.append(location)
        self.feature_set_size_to_string_map[size].add(string)
        for feature in features:
            self.feature_set_size_and_feature_to_string_map[size][feature].add( (string,location) )

    def min_Y(self) -> int:
        """min_Y returns the minimum feature set size according to the paper.

        :return: minimum search range for possible strings Y
        :rtype: int
        """
        return min(self.feature_set_size_to_string_map.keys())

    def max_Y(self) -> int:
        """max_Y returns the mamimum feature set size according to the paper

        :return: maximum search range for possible strings Y
        :rtype: int
        """
        return max(self.feature_set_size_to_string_map.keys())

    def lookup_strings(self, size: int, feature: str) -> Multiset:
        """lookup_strings finds potential canidate strings from our DB.

        :param size: feature size that we are looking through
        :type size: int
        :param feature: The features of the string
        :type feature: str
        :return: The canidate (string,location) pairs
        :rtype: Multiset
        """
        return self.feature_set_size_and_feature_to_string_map[size][feature]
################################## Searcher ###################################
class Searcher(object):
    """Searcher is the searching module for our db."""
    def __init__(self, db: RamDatabase, sim_measure: BaseSimilarity):
        self.db = db
        self.sim_measure = sim_measure
        self.feature_extractor = db.feature_extractor
        self.lookup_strings_result = defaultdict(dict)

    def search(self, query_string: str, alpha: float) -> List[Tuple[str, str]]:
        """search performs the `search` operation to find all matches

        :param query_string: string to match against
        :type query_string: str
        :param alpha: similarity threshold
        :type alpha: float
        :return: List of all returned matches
        :rtype: List[Tuple[str, str]]
        """
        features = self.feature_extractor.features(query_string)
        min_feature_size = self.sim_measure.min_Y(len(features), alpha)
        max_feature_size = self.sim_measure.max_Y(len(features), alpha)
        results = []

        for candidate_feature_size in range(min_feature_size, max_feature_size + 1):
            tau = self._min_overlap(len(features), candidate_feature_size, alpha)
            results.extend(self._tau_overlap_join(features, tau, candidate_feature_size))

        return results

    def ranked_search(self, query_string: str, alpha: float) -> List[Tuple[float, Tuple[str, str]]]:
        """ranked_search [performs the `search` operation to find all matches

        :param query_string: string to match against
        :type query_string: str
        :param alpha: similarity threshold
        :type alpha: float
        :return: List of all returned matches with scores
        :rtype: List[Tuple[float, Tuple[str, str]]]
        """
        results = self.search(query_string, alpha)
        features = self.feature_extractor.features(query_string)
        results_with_score = list(map(lambda x: [self.sim_measure.similarity(features, self.feature_extractor.features(x[0])), x], results))
        return sorted(results_with_score, key=lambda x: (-x[0], x[1]))

    def _min_overlap(self, query_size: int, candidate_feature_size: int, alpha: float) -> int:
        """_min_overlap returns the minimum overlap between the features needed

        :param query_size: size of the features of the query string
        :type query_size: int
        :param candidate_feature_size: size of the features of the candidates
        :type candidate_feature_size: int
        :param alpha: similarity threshold
        :type alpha: float
        :return: the minimum number of common features needed.
        :rtype: int
        """
        return self.sim_measure.tau(query_size, candidate_feature_size, alpha)

    def _tau_overlap_join(self, features: List[str], tau: int, candidate_feature_size: int) -> List[Tuple[str, str]]:
        """_tau_overlap_join finds all sets that intersect in at least tau features

        :param features: [description]
        :type features: List[str]
        :param tau: [description]
        :type tau: int
        :param candidate_feature_size: [description]
        :type candidate_feature_size: int
        :return: [description]
        :rtype: List[Tuple[str, str]]

        .. note::
            This uses the CPMerge algorithm to perform the tau overlap join.

        .. seealso::
            This paper is the first one that creates the tau overlap join,
            https://www.cse.iitb.ac.in/~sunita/papers/sigmod04.pdf.
        """
        query_feature_size = len(features)
        sorted_features = sorted(features, key=lambda x: len(self._lookup_strings(candidate_feature_size, x)))
        candidate_string_to_matched_count = defaultdict(int)
        results = []

        for feature in sorted_features[0:query_feature_size - tau + 1]:
            for s in self._lookup_strings(candidate_feature_size, feature):
                candidate_string_to_matched_count[s] += 1

        for s in candidate_string_to_matched_count.keys():
            for i in range(query_feature_size - tau + 1, query_feature_size):
                feature = sorted_features[i]
                if s in self._lookup_strings(candidate_feature_size, feature):
                    candidate_string_to_matched_count[s] += 1
                if candidate_string_to_matched_count[s] >= tau:
                    results.append(s)
                    break
                remaining_feature_count = query_feature_size - i - 1
                if candidate_string_to_matched_count[s] + remaining_feature_count < tau:
                    break
        return results

    def _lookup_strings(self, feature_size: int, feature: str) -> Multiset:
        """_lookup_strings finds potential canidate strings from our cache or DB.

        :param feature_size: feature size that we are looking through
        :type feature_size: int
        :param feature: The features of the string
        :type feature: str
        :return: The canidate (string,location) pairs
        :rtype: Multiset
        """
        if not (feature in self.lookup_strings_result[feature_size]):
            self.lookup_strings_result[feature_size][feature] = self.db.lookup_strings(feature_size, feature)
        return self.lookup_strings_result[feature_size][feature]
