from KB_function.DocumentLoader import DocumentLoader
from KB_function.ContentIndex import ContextIndex

import os

def find_str(input, all_files):
    for f in all_files:
        find_Result = f.find(input)
        if find_Result != -1:
            return f
    return "not found"

def AddFile(loader, docx_file, short_name): ## add a file to the existing knowledge base, according to kb_configs.py
    indexstore = ContextIndex()
    indexstore.load()
    ## load a file and add it to the knowledge base
    text = loader.ReadDataToDocs(docx_file, short_name)
    indexstore.AddFiles(text, short_name)


## create model
loader = DocumentLoader()
docx_path = "D:/LLM/KnowledgeBase/ICRP80-153MD/ICRP80-153MD"
file_names = os.listdir(docx_path)
specific_files = [101]
for pub in specific_files:
    if pub != 103:
        ICRP_pub = "101B"
        docx_file = find_str(ICRP_pub, file_names)
        short_name = "ICRP " + "101B"
        if docx_file != "not found":
            print("Converting " + docx_file + ", with name: " + short_name)
            AddFile(loader, docx_path + "/" + docx_file, short_name)

