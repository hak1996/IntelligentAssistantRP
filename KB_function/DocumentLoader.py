
from llama_index.core import SimpleDirectoryReader
#require pip install docx2txt

import configs

class DocumentLoader():
    def __init__(self):
        self.count = 0

    def ReadDataToDocs(self, path, short_name):
        documents = SimpleDirectoryReader(input_files=[path]).load_data()
        count = 0
        for doc in documents:
            del doc.metadata['file_path']
            doc.metadata['file_name'] = short_name
            doc.metadata['ch_id'] = str(count)
            count += 1
        #documents[0].metadata["file_name"] = short_name
        return documents






if __name__ == "__main__":
    doc_file = "E:/GitHub/KB_llama_index/KB_function/test.docx"
    loader = DocumentLoader()
    doc = loader.ReadDataToDocs(doc_file, "test")
    print(doc[0].metadata["src_name"])