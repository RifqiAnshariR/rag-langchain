from langchain_community.document_loaders import PyMuPDFLoader

def load_data(file_path):
    loader = PyMuPDFLoader(
        file_path=file_path,
        mode="page",
        extract_images=True,
        extract_tables="markdown"
    )
    return loader.load()
