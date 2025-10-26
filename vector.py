from typing import Tuple
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd


class VectorStoreService:
    def __init__(
            self,
            csv_path: str,
            db_path: str,
            model_embedding_name: str,
            collection_name: str,
            search_type: str,
            search_kwargs: dict,
    ):
        self.csv_path = csv_path
        self.db_path = db_path
        self.model_embedding_name = model_embedding_name
        self.collection_name = collection_name
        self.search_type = search_type
        self.search_kwargs = search_kwargs

        self.embeddings = OllamaEmbeddings(model=self.model_embedding_name)
        self.vector_store = None
        self.retriever = None

        self._initialize()

    def _initialize(self):
        """initialize embedding, vector store, and load data if needed"""

        # check if folder exists and not empty
        add_documents = False
        if not os.path.exists(self.db_path) or len(os.listdir(self.db_path)) == 0:
            add_documents = True

        # load data csv
        df = pd.read_csv(self.csv_path)

        # create vector store
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.db_path,
            embedding_function=self.embeddings,
        )

        # add docs if not exist
        if add_documents:
            documents, ids = self._prepare_documents(df)
            self.vector_store.add_documents(documents=documents, ids=ids)

        # create retriever
        self.retriever = self.vector_store.as_retriever(
            search_type=self.search_type,
            search_kwargs=self.search_kwargs,
        )

    def _prepare_documents(self, df: pd.DataFrame) -> Tuple[list[Document], list[str]]:
        """convert dataframe row into langchain documents"""

        documents = []
        ids = []

        for i, row in df.iterrows():
            doc_id = str(i)
            document = Document(
                page_content=f"{row['Title']} {row['Review']}",
                metadata={"rating": row["Rating"], "date": row["Date"]},
                id=doc_id
            )

            ids.append(doc_id)
            documents.append(document)

        return documents, ids

    def query(self, text: str):
        """query the vector store"""
        return self.retriever.invoke(text)
