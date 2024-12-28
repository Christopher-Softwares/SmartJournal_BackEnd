from chroma.chroma_connection import ChromaDBConnectionFactory
import chromadb
import random
import string

class ChromaCollectionManager:

    def __init__(self, connectionFactory : ChromaDBConnectionFactory):
        self.client = connectionFactory.connect_to_chroma()
        

    def create_collection(self, collection_name: str = None):
        
        if collection_name is None:
            collection_name = self._generate_random_collection_name()

        if self.client:
            try:
                # Create a new collection
                self.client.get_or_create_collection(name=collection_name)
                print(f"Collection '{collection_name}' created successfully.")
                print(self.client.list_collections())
                return collection_name
            
            except Exception as e:
                print(f"Error creating collection '{collection_name}': {e}")
                return None
        else:
            print("Client not connected, cannot create collection.")
            return None


    def delete_collection(self, collection_name: str):
       
        if self.client:
            try:
                # Delete the collection
                self.client.delete_collection(name=collection_name)
                print(f"Collection '{collection_name}' deleted successfully.")
                return True
            except Exception as e:
                print(f"Error deleting collection '{collection_name}': {e}")
                return False
        else:
            print("Client not connected, cannot delete collection.")
            return False
        
    
    def _generate_random_collection_name(self, length: int = 10):
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return random_name

   