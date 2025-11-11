from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

class VectorStoreManager:
    def __init__(self, url, collection_name, model_name):
        self.db_client = QdrantClient(url=url)
        self.embed_client = HuggingFaceEmbeddings(model_name=model_name)
        self.collection_name = collection_name
        self.vector_store = self._setup_vector_store()

    # def _setup_vector_store(self):
    #     vector_size = len(self.embed_client.embed_query("sample text"))

    #     if not self.db_client.collection_exists(collection_name=self.collection_name):
    #         self.db_client.create_collection(
    #             collection_name=self.collection_name,
    #             vectors_config=VectorParams(
    #                 size=vector_size,
    #                 distance=Distance.COSINE
    #             )
    #         )

    #     return QdrantVectorStore(
    #         client=self.db_client,
    #         collection_name=self.collection_name,
    #         embedding=self.embed_client,
    #     )

    def _setup_vector_store(self, reset=True):
        vector_size = len(self.embed_client.embed_query("sample text"))

        if self.db_client.collection_exists(self.collection_name):
            if reset:
                self.db_client.delete_collection(self.collection_name)      # Handle duplicate
            else:
                return QdrantVectorStore(
                    client=self.db_client,
                    collection_name=self.collection_name,
                    embedding=self.embed_client,
                )

        self.db_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

        return QdrantVectorStore(
            client=self.db_client,
            collection_name=self.collection_name,
            embedding=self.embed_client,
        )

    def add_data(self, data):
        ids = [str(uuid4()) for _ in range(len(data))]
        self.vector_store.add_documents(
            documents=data,
            ids=ids
        )

    def retrieve(self, search_type, search_kwargs):
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
