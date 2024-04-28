
#llm model
#llm_model_path = "D:/LLM/Mixtral-8x7B-Instruct-v0.1/ggml-model-q4_0.gguf"
llm_model_path = "D:/LLM/mistral-7B/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
llm_temperature = 0.0
llm_context_window = 30000
llm_max_reponse_tokens = 10000
n_gpu_layer = 50
max_new_tokens = 2560



# embedding model
embedding_model_path = "D:/LLM/BAAI/bge-base-en"
embedding_vec_len = 768
embedding_model_kwargs = {'device': 'cuda'} #{'device': 'cpu'}

# rerank model
rerank_model_path = "D:/LLM/BAAI/bge-reranker-base"
