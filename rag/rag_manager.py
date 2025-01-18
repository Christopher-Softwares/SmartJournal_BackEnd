from rag.rag_settings import RagSettings
from rag.chroma.chroma_connection import ChromaDBConnectionFactory

from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4
from langchain.llms import OpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain


class RagManager:

    def __init__(self, chroma_connection_factory : ChromaDBConnectionFactory, rag_settings : RagSettings) -> None:
        self.chroma_client = chroma_connection_factory.connect_to_chroma()
        self.rag_settings = rag_settings
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key = self.rag_settings.openai_api_key)


    def add_new_content(self, content : str, collection_name : str):

        #chunking
        text_splitter = CharacterTextSplitter(chunk_size = self.rag_settings.chunk_size, chunk_overlap = 20)
        chunks = text_splitter.split_text(content)

        docs = []
        ids = []
        for chunk in chunks:
            docs.append(Document(page_content = chunk))
            ids.append(str(uuid4()))

        vector_store = Chroma(
            client = self.chroma_client,
            collection_name = collection_name,
            embedding_function = self.embeddings,
        )
 
        vector_store.add_documents(documents = docs, ids = ids)

    
    def new_prompt(self, prompt : str, collection_name : str):
        
        vector_store = Chroma(
            client = self.chroma_client,
            collection_name = collection_name,
            embedding_function = self.embeddings
        )

        retriever = vector_store.as_retriever(
            search_type= 'mmr',
            search_kwargs={'k':4},
        )

        llm = OpenAI(temperature = 0, openai_api_key = self.rag_settings.openai_api_key)

        memory = ConversationSummaryMemory(llm=llm, memory_key='chat_history', return_messages=True)
        qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory = memory)

        result = qa(prompt)
        return result['answer']





        





        


        