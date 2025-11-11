import unicodedata
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DataProcessor:
    def __init__(self, patterns):
        self.patterns = patterns

    def _clean_data(self, data):
        cleaned_data = []
        for d in data:
            content = d.page_content
            metadata = d.metadata

            content = unicodedata.normalize('NFKC', content)
            content = self.patterns[0].sub('', content)
            content = self.patterns[1].sub('', content)
            content = self.patterns[2].sub(' ', content)
            content = self.patterns[3].sub(' ', content)
            content = self.patterns[4].sub(' ', content)
            content = self.patterns[5].sub('', content)

            cleaned_data.append(Document(page_content=content, metadata=metadata))
        
        cleaned_data = [d for i, d in enumerate(cleaned_data) if i not in (1, 2)]
        return cleaned_data

    def _split_text(self, data, chunk_size, chunk_overlap):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return text_splitter.split_documents(data)

    def process(self, raw_data, chunk_size, chunk_overlap):
        cleaned_data = self._clean_data(raw_data)
        splitted_data = self._split_text(cleaned_data, chunk_size, chunk_overlap)
        return splitted_data
