
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.prompts import PromptTemplate

from KB_function.LLM_Model import LLM_Model
from KB_function.ContentIndexSimple import ContextIndex
from KB_function import Prompts
from KB_function.Reranker import Reranker

class RetriverQuery():
    def __init__(self):
        self.llm = LLM_Model()
        self.vectorindex = ContextIndex()
        index = self.vectorindex.LoadWithLLM(self.llm.get_llm())
        self.index = index
        self.reranker = Reranker()

        self.use_rerank = False
        self.topk = 5
        self.topn = 2

    def ConstructContext(self):

        retriever_chunk = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.topk,
        )

        qa_template = PromptTemplate(Prompts.RAG_template)
        #prompt = qa_template.format(context_str=..., query_str=...)

        if self.use_rerank:
            self.reranker.set_top_n(self.topn)
            self.query_engine_chunk = RetrieverQueryEngine.from_args(
                retriever_chunk,
                node_postprocessors = [self.reranker],
                verbose=True)
        else:
            self.query_engine_chunk = RetrieverQueryEngine.from_args(
                retriever_chunk,
                verbose=True)


        #QA_PROMPT_KEY = "response_synthesizer:text_qa_template"
        #print(self.query_engine_chunk.get_prompts()[QA_PROMPT_KEY].get_template())

        self.query_engine_chunk.update_prompts(
            {"response_synthesizer:text_qa_template": qa_template}
        )

    def query(self, query):
        response = self.query_engine_chunk.query(query)
        ref = ""
        for node in response.source_nodes:
           ref += node.metadata["file_name"] + ": \n\n"
           ref += node.get_content()
           ref += "\n\n"

        reply = response.response
        reference = ref
        return  reply, reference

    def set_use_rerank(self, use_rerank):
        self.use_rerank = use_rerank

    def set_topk(self, topk):
        self.topk = topk

    def set_topn(self, topn):
        self.topn = topn

if __name__ == "__main__":
    assist = RetriverQuery()
    assist.ConstructContext()
    r, ref = assist.query("how to partition a document")
    print(r)
    print(ref)