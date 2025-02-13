from typing import Iterator, List

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore

from langchain_cfg_build.embed_db.embed_db_loader import EmbedDbLoader


def save_embed_db(db_loader: EmbedDbLoader, doc_iterator: Iterator[List[Document]]) :
    v_store: VectorStore = db_loader.load()
    for doc_list in doc_iterator:
        v_store.add_documents(doc_list)


def _test_document_generator() -> Iterator[List[Document]]:
    # Imagine this function pulls documents from a database or some other source
    for i in range(20):  # Example of generating 1000 batches
        print(f"Generating {i}")
        yield [Document(
            page_content=f"1This is document {i + 1}. It contains some sample text.",
            metadata={"source_url": f"https://1example.com/document/{i + 1}"}
        ), Document(
            page_content=f"1This is another document {i + 1}. It contains more sample text.",
            metadata={"source_url": f"https://2example.com/document/{i + 1}"}
        )]


def trim_metadata_dict(input_dict: dict) -> dict:
    """
    Recursively trims a dictionary to ensure all values are of type str, int, float, or bool.
    It removes any entries that do not conform to these types.
    """
    return {key: value for key, value in input_dict.items()
            if isinstance(value, (str, int, float, bool))}
