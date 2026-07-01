import os
import requests
import json
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class vec_db():
    """
    A class wrapper to download a product catalog, build a local 
    vector database using ChromaDB, and handle semantic queries.
    """
    def __init__(self):
        self._chroma_client = chromadb.Client()
        self._get_catalog()
        self._build_database(collection_name= "catalog_collection")

    def query(self, texts, collection_name="catalog_collection", n_results=5):
        """
        Queries the vector database to find the most relevant entries.

        Parameters:
        - texts (list of str): The search queries.
        - collection_name (str): The collection to search in.
        - n_results (int): Number of top matching results to return.
        """
        collection = self._chroma_client.get_collection(name=collection_name)

        return collection.query(
            query_texts=texts,
            n_results=n_results
        )

    def _build_database(self, collection_name= "collection"):
        """
        Reads the local JSON catalog, processes the text fields into structured 
        documents, extracts metadata, and stores them in a ChromaDB collection.
        """

        with open("catalog_data.json","r") as file:
            data = json.load(file)

        embedding_fn = SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        collection = self._chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_fn,
        )

        ids = []
        documents = []
        metadatas = []

        for item in data:
            ids.append(str(item["entity_id"]))

            documents.append(
                f"""
                Name: {item['name']}
                Description: {item['description']}
                Job Levels: {", ".join(item['job_levels'])}
                Skills: {", ".join(item['keys'])}
                Languages: {", ".join(item['languages'])}
                Duration: {item['duration']}
                Remote: {item['remote']}
                Adaptive: {item['adaptive']}
                """.strip()
            )

            metadatas.append({
                "name": item["name"],
                "link": item["link"],
                "remote": item["remote"],
                "adaptive": item["adaptive"],
                "duration": item["duration"],
            })

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        return collection

    def _get_catalog(self):
        """
        Internal helper: Fetches the raw SHL product catalog JSON file 
        from a remote production URL and writes it to disk.
        """
        if os.path.exists("catalog_data.json"):
            return None
        url = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"
        response = requests.get(url)
        with open("catalog_data.json","w") as file:
            file.write(response.text)

        return None
    
vectordb = vec_db()
