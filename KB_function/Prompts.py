

RAG_template = (
    "We have provided context information below. \n"
    "<context>\n"
    "{context_str}\n"
    "</context>\n"   
    "Given this information, please answer the query in detail.\n"
    "Query: {query_str}"
    "Answer:")
