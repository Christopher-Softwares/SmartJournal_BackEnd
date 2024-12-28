class RagSettings:
    def __init__(self, openai_api_key: str, chunk_size):
        self.openai_api_key = openai_api_key
        self.chunk_size = chunk_size