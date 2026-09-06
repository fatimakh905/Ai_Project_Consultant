from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


PDF_FOLDER = Path("data/pdfs")


def load_documents():
    documents = []

    for pdf_file in PDF_FOLDER.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        docs = loader.load()

        documents.extend(docs)

        print(f"Loaded: {pdf_file.name} | Pages: {len(docs)}")

    print(f"\nTotal pages loaded: {len(documents)}")

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print("\nFirst document:")
    print(documents[0].page_content[:500])