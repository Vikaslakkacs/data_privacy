import os
from dotenv import load_dotenv
from operator import itemgetter
from src.data_privacy.utils.utils import load_document
### anonymization libraries
from faker import Faker
from presidio_analyzer import Pattern, PatternRecognizer
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
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

##Guard rails library
from nemoguardrails import LLMRails, RailsConfig
from data_privacy.guardrails.guardrails import guardrails
import asyncio
### Anonymization  
class anonymization():
    def __init__(self, doc_path, synthetic_data:bool):
        self.documents= load_document(doc_path)
        self.anonymizer= self._initate_anonymizer(synthetic_data)
        load_dotenv()
        self.OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
    
    def _initate_anonymizer(self, synthetic_data:bool):
        anonymizer= PresidioReversibleAnonymizer(
            add_default_faker_operators=synthetic_data
        )
        ##rest all the mappings
        anonymizer.reset_deanonymizer_mapping()
        return anonymizer
    
    def _anonymize_data_chunks(self):
        """Anonymize data before indexing
        """
        
        for doc in self.documents:
            doc.page_content= self.anonymizer.anonymize(doc.page_content) 
        ## Split the document into chunks
        text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks= text_splitter.split_documents(self.documents)
        return chunks
    
    def get_retriever(self):
        """creating retrievers from chunks of documents using FAISS vector DB
        """
        chunks= self._anonymize_data_chunks()
        
        ##Create embeddings
        embeddings= OpenAIEmbeddings()
        docsearch= FAISS.from_documents(chunks, embeddings)
        
        retriever= docsearch.as_retriever()
        return retriever
    
    def _template(self):
        template="""" Answer the question based only on the following context:
                        {context}

                        Question: {anonymized_question}
                        """
        return template
    

    def initiate_anonymize_model(self):
        """Initiate model by defining models, prompts, templates and all the chains.
        """
        ##Get the retriever
        retriever= self.get_retriever()
        template= self._template()
        prompt= ChatPromptTemplate.from_template(template= template)
        
        ##Model defining 
        ## Initiate from Guardrails
        #model= ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo')
        
        guardrails_initiate= guardrails("/Users/vikaslakka/Desktop/FSDS/GenAI/poc/data_privacy/data_privacy/config")
        rails=guardrails_initiate.initiate_rails()

        
        
        ##Define Runnable parameters
        ##Make sure you anonymize question as well.
        inputs= RunnableParallel(
            question= RunnablePassthrough(),
            anonymized_question= RunnableLambda(self.anonymizer.anonymize),            
        )
        
        ## Create anonymize chain
        ## fill the parameters from templatealong with inputs
        
        anonymize_chain= (
            inputs
            | {'context':itemgetter("anonymized_question")
               |retriever,
               'anonymized_question': itemgetter("anonymized_question"),
               }
            |prompt
            |rails.llm
            |StrOutputParser()
        )
        ## Register anoymize chain into guardrails
        self.create_guardrails_function(rails, anonymize_chain)
        
        #return anonymize_chain
        return rails
    
    def create_guardrails_function(self,rails, anonymize_chain):
        async def get_guardrails_result(question):
            return anonymize_chain.invoke(question)
        
        ##Register function into Guardrails LLM
        rails.register_action(get_guardrails_result, name="qa_chain")
        

    def initiate_deanonymize_model(self, response):
        """We will take response of the chain and de anonymize it.
        """
        return self.anonymizer.deanonymize(response)
    
        
        
if __name__=="__main__":
    anon= anonymization("/Users/vikaslakka/Desktop/FSDS/GenAI/poc/data_privacy/data_privacy/cases/theft_case.txt",
                        synthetic_data=True)
    anonymize_chain= anon.initiate_anonymize_model()
    #deanonymize_chain= anon.initiate_deanonymize_model()
    
    while True:
        ques= input("Ask about the scene: ")
        if ques=='exit':
            break
        else:
            from pprint import pprint
            print(asyncio.run( anonymize_chain.generate_async(ques)))
            #print(asyncio.run( deanonymize_chain.generate_async(ques)))
            #pprint(anon.anonymizer.deanonymizer_mapping)
            print('\n\n\n')
            #print(deanonymize_chain.invoke(ques))
    