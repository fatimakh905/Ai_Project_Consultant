from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.document_loader import load_documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    return chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)

    print("\nFirst chunk:")
    print(chunks[0].page_content)

    print("\nFirst chunk metadata:")
    print(chunks[0].metadata)