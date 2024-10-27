"""
Lab 2.

Text retrieval with BM25
"""


from docutils.nodes import document
from sphinx.cmd.quickstart import nonempty
from math import log
# pylint:disable=too-many-arguments, unused-argument


def tokenize(text: str) -> list[str] | None:
    """
    Tokenize the input text into lowercase words without punctuation, digits and other symbols.

    Args:
        text (str): The input text to tokenize.

    Returns:
        list[str] | None: A list of words from the text.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(text, str) or not text:
        return None
    result = ""
    for elem in text.lower():
        if elem.isalpha() is True:
            result += elem
            continue
        result += " "
    tokens1 = result.split(" ")
    tokens2 = []
    for elem in tokens1:
        if elem.isalpha() is True:
            tokens2.append(elem)
    return tokens2



def remove_stopwords(tokens: list[str], stopwords: list[str]) -> list[str] | None:
    """
    Remove stopwords from the list of tokens.

    Args:
        tokens (list[str]): List of tokens.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[str] | None: Tokens after removing stopwords.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(tokens, list) or not isinstance(stopwords, list) or not all(isinstance(symbol, str) for symbol in tokens) or not all(isinstance(symb, str) for symb in stopwords) or not tokens or not stopwords:
        return None
    filtered_tokens = [word for word in tokens if word not in stopwords]
    return filtered_tokens


def build_vocabulary(documents: list[list[str]]) -> list[str] | None:
    """
    Build a vocabulary from the documents.

    Args:
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        list[str] | None: List with unique words from the documents.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(documents, list) or not documents:
        return None
    unique_voc = set()
    for tokens_list in documents:
        if not isinstance(tokens_list, list):
            return None
        for token in tokens_list:
            if not isinstance(token, str):
                return None
        unique_voc.update(tokens_list)
    return list(unique_voc)


def calculate_tf(vocab: list[str], document_tokens: list[str]) -> dict[str, float] | None:
    """
    Calculate term frequency for the given tokens based on the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        document_tokens (list[str]): Tokenized document.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to their term frequency.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(vocab, list) or not all(isinstance(item, str) for item in vocab) or not vocab or not isinstance(document_tokens, list) or not all(isinstance(item, str) for item in document_tokens) or not document_tokens:
        return None
    tf_result = {}
    union = set(vocab).union(set(document_tokens))
    for word in union:
        tf_result[word] = document_tokens.count(word) / len(document_tokens)
    return tf_result


def calculate_idf(vocab: list[str], documents: list[list[str]]) -> dict[str, float] | None:
    """
    Calculate inverse document frequency for each term in the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to its IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(vocab, list) or not all(isinstance(item, str) for item in vocab) or not isinstance(documents, list) or not all(isinstance(docum, list) for docum in documents) or not all(isinstance(item, str) for docum in documents for item in docum) or not vocab or not documents:
        return None
    idf_result = {}
    doc_num = len(documents)
    for word in vocab:
        words_count = sum(1 for doc in documents if word in doc)
        idf_result[word] = log((doc_num - words_count + 0.5) / (words_count + 0.5))
    return idf_result


def calculate_tf_idf(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float] | None:
    """
    Calculate TF-IDF scores for a document.

    Args:
        tf (dict[str, float]): Term frequencies for the document.
        idf (dict[str, float]): Inverse document frequencies.

    Returns:
        dict[str, float] | None: Mapping from terms to their TF-IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(tf, dict) or not isinstance(idf, dict) or not all(isinstance(key, str) for key in tf) or not all(isinstance(key, str) for key in idf) or not all(isinstance(value, float) for value in tf.values()) or not all(isinstance(value, float) for value in idf.values()) or not tf or not idf:
        return None
    tf_idf_result = {}
    for word in tf:
        tf_idf_result[word] = tf[word] * idf[word]
    return tf_idf_result


def calculate_bm25(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores.

    In case of corrupt input arguments, None is returned.
    """
    if not vocab or not all(isinstance(vocab, list)) or not all(isinstance(element, str) for element in vocab):
        return None
    if not document or not all(isinstance(document, list)) or not all(isinstance(element, str) for element in document):
        return None
    if not idf_document or not isinstance(idf_document, dict) or not all(isinstance(key, str) for key in idf_document) or not all(isinstance(value, float) for value in idf_document.values()):
        return None
    if not isinstance(avg_doc_len, float) or not isinstance(doc_len, int) or not isinstance(doc_len, bool) or not isinstance(k1, float) or not isinstance(b, float):
        return None
    bm25_res = {}
    for element in set(vocab).union(set(document)):
        if element in idf_document:
            element_count = document.count(element)
            bm25_res[element] = idf_document[element] * ((element_count * (k1 + 1)) / element_count + k1 * (1 - b + (b * doc_len / avg_doc_len)))
        else:
            bm25_res[element] = 0.0
    return bm25_res


def rank_documents(
    indexes: list[dict[str, float]], query: str, stopwords: list[str]
) -> list[tuple[int, float]] | None:
    """
    Rank documents for the given query.

    Args:
        indexes (list[dict[str, float]]): List of BM25 or TF-IDF indexes for the documents.
        query (str): The query string.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[tuple[int, float]] | None: Tuples of document index and its score in the ranking.

    In case of corrupt input arguments, None is returned.
    """
    if not indexes or not isinstance(indexes, list) or not all(isinstance(element, dict) for element in indexes) or not all(isinstance(key, str) for element in indexes for key in element) or not all(isinstance(value, float) for element in indexes for value in element.values()):
        return None
    if not isinstance(query, str) or not isinstance(stopwords, list) or not all(isinstance(element, str) for element in stopwords):
        return None
    query_1_step = tokenize(query)
    if query_1_step is None:
        return None
    query_2_step = remove_stopwords(query_1_step, stopwords)
    if query_2_step is None:
        return None
    result = []
    for i, document in enumerate(indexes):
        result.append((i, sum(document[element] if element in document else 0 for element in query_2_step)))
        return sorted(result, reverse=True, key=lambda tuple_: tuple_[1])


def calculate_bm25_with_cutoff(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    alpha: float,
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document with IDF cutoff.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        alpha (float): IDF cutoff threshold.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores with cutoff applied.

    In case of corrupt input arguments, None is returned.
    """


def save_index(index: list[dict[str, float]], file_path: str) -> None:
    """
    Save the index to a file.

    Args:
        index (list[dict[str, float]]): The index to save.
        file_path (str): The path to the file where the index will be saved.
    """


def load_index(file_path: str) -> list[dict[str, float]] | None:
    """
    Load the index from a file.

    Args:
        file_path (str): The path to the file from which to load the index.

    Returns:
        list[dict[str, float]] | None: The loaded index.

    In case of corrupt input arguments, None is returned.
    """


def calculate_spearman(rank: list[int], golden_rank: list[int]) -> float | None:
    """
    Calculate Spearman's rank correlation coefficient between two rankings.

    Args:
        rank (list[int]): Ranked list of document indices.
        golden_rank (list[int]): Golden ranked list of document indices.

    Returns:
        float | None: Spearman's rank correlation coefficient.

    In case of corrupt input arguments, None is returned.
    """