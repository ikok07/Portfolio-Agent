from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

class TextSplitter:

    @staticmethod
    def markdown_split(texts: list[str]) -> list[Document]:
        split_headers = [
            ("#", "Header 1"),
            ("##", "Header 2")
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(split_headers)

        splitted_markdowns: list[Document] = [
            doc
            for text in texts
            for doc in markdown_splitter.split_text(text)
        ]
        
        return splitted_markdowns

    @staticmethod
    def generic_split(texts: list[str]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
        splitted_texts: list[Document] = [
            Document(doc)
            for text in texts
            for doc in text_splitter.split_text(text)
        ]

        return splitted_texts
