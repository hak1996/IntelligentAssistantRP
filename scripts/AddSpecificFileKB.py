from KB_function.DocumentLoader import DocumentLoader
from KB_function.ContentIndexSimple import ContextIndex


def AddFile(loader, docx_file, short_name): ## add a file to the existing knowledge base, according to kb_configs.py
    indexstore = ContextIndex()
    indexstore.load()
    ## load a file and add it to the knowledge base
    text = loader.ReadDataToDocs(docx_file, short_name)
    indexstore.AddFiles(text, short_name)


## create model
loader = DocumentLoader()

file_name = "your file name"
short_name = "your short name"
AddFile(loader, file_name, short_name)

