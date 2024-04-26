
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from llama_index.core.schema import NodeWithScore
from llama_index.core.schema import QueryBundle
from typing import List, Optional

from llama_index.core.postprocessor.types import BaseNodePostprocessor


import configs

class Reranker(BaseNodePostprocessor):
    top_n = 1
    tokenizer = AutoTokenizer.from_pretrained(configs.rerank_model_path)
    model = AutoModelForSequenceClassification.from_pretrained(configs.rerank_model_path)
    model.eval()

    def set_top_n(self,topn):
        self.top_n = topn


    def get_score(self, query, answers): # input the string of query and anwsers
        pairs = [[query, answer] for answer in answers]
        with torch.no_grad():
            inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores = self.model(**inputs, return_dict=True).logits.view(-1, ).float()
        return scores

    def print_info(self):
        print(self.top_n)

    def _postprocess_nodes(
            self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle]
    ) -> List[NodeWithScore]:
        query = query_bundle.query_str
        answers = [node.get_content() for node in nodes]
        scores = self.get_score(query, answers)
        initial_results = nodes
        for i, score in enumerate(scores):
            initial_results[i].score = score
        sorted(initial_results, key=lambda x: x.score or 0.0, reverse=True)
        return initial_results[:self.top_n]

if __name__ == "__main__":
    reranker = Reranker()
    reranker.print_info()



