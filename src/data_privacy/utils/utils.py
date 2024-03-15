import os
from langchain_core.documents import Document

###loading documents
def load_document(path) -> list:
    """takes the path of the file and generates doc strings.

    Args:
        path (string): Generate document from text data(currently)
    """
    with open(path, 'r') as doc_text:
        document=[Document(page_content= doc_text.read())]
        return document