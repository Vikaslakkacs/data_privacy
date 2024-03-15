import os
from langchain_core.documents import Document

###loading documents
def load_document(path) -> list:
    """takes the path of the file and generates doc strings.

    Args:
        path (string): Generate document from text data(currently)
    """
    print(f"Helloooooooooooooooooooo:")
    document=[Document(page_content= path.read().decode("utf-8"))]
    return document
    if type(path)=='str':
        with open(path, 'r') as doc_text:
            document=[Document(page_content= doc_text.read())]
            return document
    else:
        document=[Document(page_content= path.read().decode("utf-8"))]
        return document