
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.prompts import PromptTemplate

from KB_function.LLM_Model import LLM_Model
from KB_function.ContentIndex import ContextIndex
from KB_function import Prompts

class RetriverQuery():
    def __init__(self):
        self.llm = LLM_Model()
        self.vectorindex = ContextIndex()
        index, node_dict = self.vectorindex.LoadWithLLM(self.llm.get_llm())
        self.index = index
        self.node_dict = node_dict


    def ConstructContext(self, topk):
        vector_retriever_chunk = self.index.as_retriever(similarity_top_k=topk)

        retriever_chunk = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": vector_retriever_chunk},
            node_dict=self.node_dict,
            verbose=True,
        )

        qa_template = PromptTemplate(Prompts.RAG_template)
        prompt = qa_template.format(context_str=..., query_str=...)

        self.query_engine_chunk = RetrieverQueryEngine.from_args(
            retriever_chunk
        )

        #QA_PROMPT_KEY = "response_synthesizer:text_qa_template"
        #print(self.query_engine_chunk.get_prompts()[QA_PROMPT_KEY].get_template())

        self.query_engine_chunk.update_prompts(
            {"response_synthesizer:text_qa_template": qa_template}
        )

    def query(self, query): #streaming response
        response = self.query_engine_chunk.query(query)
        ref = "References:\n\n"
        for node in response.source_nodes:
            ref += node.metadata["file_name"] + ": \n\n"
            ref += node.get_content()
            ref += "\n\n"

        print(ref)
        return response.response, ref