
#llm model
llm_model_path = # path to llm
# setup for llm
llm_temperature = 0.0
llm_context_window = 30000
llm_max_reponse_tokens = 10000
n_gpu_layer = 50
max_new_tokens = 2560



# embedding model
embedding_model_path = #path to embedding model
embedding_vec_len = 768
embedding_model_kwargs = {'device': 'cuda'} #{'device': 'cpu'}

# rerank model
rerank_model_path = # path to reranking model

