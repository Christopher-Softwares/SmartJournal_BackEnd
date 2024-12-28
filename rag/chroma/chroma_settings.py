class ChromaDBConnectionSettings:
    def __init__(self, is_internal, host, port, local_dir):
        self.is_internal = is_internal
        self.host = host
        self.port = port
        self.local_dir = local_dir
       

    def get_connection_url(self):
        scheme = "https"
        connection_url = f"{scheme}://{self.host}:{self.port}"

        return connection_url

