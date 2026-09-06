from langchain_chroma import Chroma
from src.embeddings import get_embedding_model

CHROMA_DIR = "chroma_db"


def test_retrieval():
    print("Loading embedding model...")
    embedding_model = get_embedding_model()

    print("Opening existing Chroma database...")
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    )

    print(f"Total stored chunks: {vector_store._collection.count()}")

    question = "How much does a RAG-based knowledge assistant cost?"

    print(f"\nQuestion: {question}")

    results = vector_store.similarity_search(
        question,
        k=3
    )

    print("\nTop 3 relevant chunks:\n")

    for i, doc in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(doc.page_content)
        print("\nMetadata:")
        print(doc.metadata)
        print()


if __name__ == "__main__":
    test_retrieval()