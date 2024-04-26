
from KB_function.DocumentLoader import DocumentLoader
from KB_function.ContentIndexSimple import ContextIndex
import os

#import a set of documents to your constructed knowledge database

def AddFile(loader, docx_file, short_name): ## add a file to the existing knowledge base, according to kb_configs.py
    indexstore = ContextIndex()
    indexstore.load()
    ## load a file and add it to the knowledge base
    text = loader.ReadDataToDocs(docx_file, short_name)
    indexstore.AddFiles(text, short_name)


## create model
loader = DocumentLoader()
doc_dir = # direction of your documents
file_names = os.listdir(doc_dir)
for i, file in enumerate(file_names):
    if i>0:
        filename = doc_dir + "/" + file
        short_name = file[:-5] #set it yourself

        print("Converting " + file + ", with name: " + short_name)
        AddFile(loader, filename, short_name)
