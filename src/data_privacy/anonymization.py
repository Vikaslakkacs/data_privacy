import os
from dotenv import load_dotenv
from operator import itemgetter
from data_privacy.utils import *
##Lang chain libraries
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel
)
from langchain_openai import ChatOpenAI

### Anonymization
class anonymization:
    def __init__(self, doc_path:str):
        self.documents= load_document(doc_path)

anon= anonymization("/Users/vikaslakka/Desktop/FSDS/GenAI/poc/data_privacy/data_privacy/cases/theft_case.txt")
print(anon.documents)