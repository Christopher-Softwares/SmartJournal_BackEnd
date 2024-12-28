import chromadb
from chroma.chroma_settings import ChromaDBConnectionSettings
from chromadb.config import Settings

class ChromaDBConnectionFactory:

    def __init__(self, settings : ChromaDBConnectionSettings):
        self.settings = settings

    def connect_to_chroma(self):
        # Get the connection URL from the settings
        connection_url = self.settings.get_connection_url()
        
        try:
        
            if self.settings.is_internal == False:
                print(f"Attempting to connect to Chroma DB at: {connection_url}")
                client = chromadb.HttpClient(self.settings.host, self.settings.port)
                print(f"Connected to Chroma DB at {connection_url}")

            else:
                print(f"Attempting to connect to Chroma DB at localhost")
                client = chromadb.PersistentClient(path=self.settings.local_dir)
                print(f"Connected to Chroma DB at local host")

            
            return client

        except Exception as e:
            print(f"Error connecting to Chroma DB: {e}")
            return None