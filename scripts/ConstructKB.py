from KB_function.DocumentLoader import DocumentLoader
from KB_function.ContentIndexSimple import ContextIndex

import os

doc_dir = #dirction of your documents
file_list = os.listdir(docx_dir)

loader = DocumentLoader()

doc_file = doc_dir + "/" + file_list[0]
short_name = (file_list[0])[:-5]  # the name of document recorded in your knowledge database, it can be set by yourself

text = loader.ReadDataToDocs(doc_file, short_name)

indexstore = ContextIndex()
indexstore.Construct(text, short_name)
