
from KB_function.CustomLlamaCpp import LlamaCPP


import configs

class LLM_Model():
    def __init__(self):
        if configs.n_gpu_layer>1: #use gpu
            self.llm = LlamaCPP(
                model_path=configs.llm_model_path,
                temperature=configs.llm_temperature,
                max_new_tokens=configs.max_new_tokens,
                context_window=configs.llm_context_window,
                model_kwargs={"n_gpu_layers": configs.n_gpu_layer},
                verbose=True)
        else:
            self.llm = LlamaCPP(
                model_path=configs.llm_model_path,
                temperature=configs.llm_temperature,
                max_new_tokens=configs.max_new_tokens,
                context_window=configs.llm_context_window,
                odel_kwargs={"n_gpu_layers": configs.n_gpu_layer},
                verbose=True)

    def get_llm(self):
        return self.llm
