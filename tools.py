from vector_db import vectordb

def search_catalog(query, n_results=5):
    """
    Searches the product catalog vector database using a text query.
    
    Parameters:
    - query (str): The keyword or phrase to search for.
    - n_results (int): The number of matching records to return.
    
    Returns:
    - dict: ChromaDB query results containing documents, metadatas, and ids.
    """

    queries = [query]

    results = vectordb.query(
        texts=queries,
        collection_name="catalog_collection",
        n_results=n_results
    )
    
    return results