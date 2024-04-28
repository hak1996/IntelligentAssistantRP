
from KB_function.DocumentLoader import DocumentLoader
from KB_function.ContentIndex import ContextIndex

loader = DocumentLoader()

docx_file = "D:/LLM/KnowledgeBase/ICRP80-153MD/ICRP80-153MD/ICRP Publication 101A.md"
short_name = "ICRP 101A"

text = loader.ReadDataToDocs(docx_file, short_name)

indexstore = ContextIndex()
indexstore.Construct(text,short_name)
