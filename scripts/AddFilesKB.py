
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
for i in range(153-80+1):
    pub = i + 80
    if pub != 101:
        ICRP_pub = str(pub)
        docx_file = find_str(ICRP_pub, file_names)
        short_name = "ICRP " + str(pub)
        if docx_file != "not found":
            print("Converting " + docx_file + ", with name: " + short_name)
            AddFile(loader, docx_path + "/" + docx_file, short_name)
