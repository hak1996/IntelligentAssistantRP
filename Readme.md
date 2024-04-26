# Demo of intelligent assistant in radiation protection

We provide a simplified demo of intelligent assistant in radiation protection. You can clone the repository and construct your intelligent assistant in radiation protection.

Before you begin, you need to download LLM and embedding and reranking model:

+ Mistral-7B: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

+ embedidding model: https://huggingface.co/BAAI/bge-base-en-v1.5

+ reranking model: https://huggingface.co /BAAI/bge-reranker-base

Then you should set the directions of your models and database.

After above steps, you can import knowledge to your assistant by using the code in "scripts" and  chat with your assistant 

'''
streamlit run webui.py
'''


