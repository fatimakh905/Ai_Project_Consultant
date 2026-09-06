from src.document_loader import load_documents
from src.text_splitter import split_documents
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store


def ingest_documents():
    print("Loading documents...")
    documents = load_documents()

    print("\nSplitting documents...")
    chunks = split_documents(documents)

    print("\nLoading embedding model...")
    embedding_model = get_embedding_model()

    print("\nCreating Chroma vector database...")
    vector_store = create_vector_store(chunks, embedding_model)

    print("\nIngestion complete!")
    print(f"Stored {len(chunks)} chunks in Chroma.")


if __name__ == "__main__":
    ingest_documents()