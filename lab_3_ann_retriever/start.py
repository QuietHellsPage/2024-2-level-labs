"""
Laboratory Work #3 starter.
"""

# pylint:disable=duplicate-code, too-many-locals, too-many-statements, unused-variable
from pathlib import Path

from pyspelling.filters.python import tokenizer

from lab_3_ann_retriever.main import BasicSearchEngine, Vectorizer, Tokenizer

def open_files() -> tuple[list[str], list[str]]:
    """
    # stubs: keep.

    Open files.

    Returns:
        tuple[list[str], list[str]]: Documents and stopwords
    """
    documents = []
    for path in sorted(Path("assets/articles").glob("*.txt")):
        with open(path, "r", encoding="utf-8") as file:
            documents.append(file.read())
    with open("assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")
    return (documents, stopwords)


def main() -> None:
    """
    Launch an implementation.
    """
    with open("assets/secrets/secret_1.txt", "r", encoding="utf-8") as text_file:
        text = text_file.read()
    result = None

    documents, stopwords = open_files()
    tokenize = Tokenizer(stopwords)

    vectorize = Vectorizer(tokenize.tokenize_documents(documents))
    vectorize.build()

    knn = BasicSearchEngine(vectorize, tokenize)
    knn.index_documents(documents)



    vector = vectorize.vectorize(tokenize.tokenize(documents[0]))
    print(vector)

    pre_vect = vectorize.vector2tokens(vector)
    print(pre_vect)

    result = knn.retrieve_vectorized(vector)
    print(result)


    assert result, "Result is None"


if __name__ == "__main__":
    main()
