from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.settings import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.schema import IndexNode


import faiss
from llama_index.vector_stores.faiss import FaissVectorStore

import json

import tqdm



from KB_function.EmbeddingModel import EmbeddingModel

import kb_configs
import configs

class ContextIndex():
    def __init__(self):
        dimension = configs.embedding_vec_len
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.vector_store = FaissVectorStore(faiss_index=self.faiss_index)
        self.storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore(),
            vector_store=self.vector_store,
            index_store=SimpleIndexStore(),
        )

    def load(self):
        self.storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore.from_persist_dir(persist_dir=kb_configs.path_kb),
            vector_store=self.vector_store.from_persist_dir(persist_dir=kb_configs.path_kb),
            index_store=SimpleIndexStore.from_persist_dir(persist_dir=kb_configs.path_kb),
        )

        with open(kb_configs.path_kb+"/node_names.json", "r") as file:
            content = file.read()
            nodes_id = json.loads(content)

        self.node_ids = nodes_id
        self.node_dict = {}
        for id in self.node_ids:
            node = self.storage_context.docstore.get_node(id)
            self.node_dict.update({id:node})

        # embedding
        embed = EmbeddingModel()
        embed_model = embed.get_model()
        Settings.llm = None
        Settings.embed_model = embed_model
        from llama_index.core.indices.loading import load_index_from_storage
        self.loaded_index = load_index_from_storage(self.storage_context)






    def Construct(self, docs, filename):
        # embedding
        embed = EmbeddingModel()
        embed_model = embed.get_model()
        Settings.llm = None
        Settings.embed_model = embed_model

        # base nodes
        base_node_parser = SentenceSplitter.from_defaults(chunk_size=kb_configs.chunk_size_base, chunk_overlap=kb_configs.chunk_overlap_base)
        base_nodes = base_node_parser.get_nodes_from_documents(docs)
        for idx, node in enumerate(base_nodes):
            node.id_ = filename + "-" + str(idx)

        # construct subnodes
        sub_node_parser = SentenceSplitter.from_defaults(chunk_size=kb_configs.chunk_size_small, chunk_overlap=kb_configs.chunk_overlap_small)
        all_nodes = []
        for base_node in base_nodes:
            sub_nodes = sub_node_parser.get_nodes_from_documents([base_node])
            sub_inodes = [IndexNode.from_text_node(sn, base_node.node_id) for sn in sub_nodes]
            all_nodes.extend(sub_inodes)
            original_node = IndexNode.from_text_node(base_node, base_node.node_id)
            all_nodes.append(original_node)

        loaded_index = VectorStoreIndex(all_nodes, storage_context=self.storage_context)

        loaded_index.storage_context.persist(kb_configs.path_kb)
        with open(kb_configs.path_kb+"/node_names.json", "w") as file:
            nodes_id = [n.node_id for n in all_nodes]
            json.dump(nodes_id, file)




    def AddFiles(self, docs, filename):
        # base nodes
        base_node_parser = SentenceSplitter.from_defaults(chunk_size=kb_configs.chunk_size_base)
        base_nodes = base_node_parser.get_nodes_from_documents(docs)
        for idx, node in enumerate(base_nodes):
            node.id_ = filename + "-" + str(idx)

        #construct subnodes
        sub_node_parser = SentenceSplitter.from_defaults(chunk_size=kb_configs.chunk_size_small)
        all_nodes = []
        for base_node in base_nodes:
            sub_nodes = sub_node_parser.get_nodes_from_documents([base_node])
            sub_inodes = [IndexNode.from_text_node(sn, base_node.node_id) for sn in sub_nodes]
            all_nodes.extend(sub_inodes)
            original_node = IndexNode.from_text_node(base_node, base_node.node_id)
            all_nodes.append(original_node)


        self.loaded_index.insert_nodes(all_nodes, storage_context=self.storage_context)

        self.loaded_index.storage_context.persist(kb_configs.path_kb)

        with open(kb_configs.path_kb+"/node_names.json", "w") as file:
            nodes_id = [n.node_id for n in all_nodes]
            nodes_id.extend(self.node_ids)
            json.dump(nodes_id, file)

    def Retriever(self, query, topk):
        '''base_retriever = self.loaded_index.as_retriever(similarity_top_k=topk)
        query_engine_base = RetrieverQueryEngine.from_args(
            base_retriever, service_context=self.service_context
        )
        response = query_engine_base.query(
            query
        )
        print(str(response))

        '''
        vector_retriever_chunk = self.loaded_index.as_retriever(similarity_top_k=topk)
        
        retriever_chunk = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": vector_retriever_chunk},
            node_dict=self.node_dict,
            verbose=True,
        )

        nodes = retriever_chunk.retrieve(
            query
        )
        for node in nodes:
            print(node)

    def LoadWithLLM(self, llm):
        self.storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore.from_persist_dir(persist_dir=kb_configs.path_kb),
            vector_store=self.vector_store.from_persist_dir(persist_dir=kb_configs.path_kb),
            index_store=SimpleIndexStore.from_persist_dir(persist_dir=kb_configs.path_kb),
        )

        with open(kb_configs.path_kb + "/node_names.json", "r") as file:
            content = file.read()
            nodes_id = json.loads(content)

        self.node_ids = nodes_id
        self.node_dict = {}
        for id in self.node_ids:
            node = self.storage_context.docstore.get_node(id)
            self.node_dict.update({id: node})

        # embedding
        embed = EmbeddingModel()
        embed_model = embed.get_model()
        Settings.llm = llm
        Settings.embed_model = embed_model
        from llama_index.core.indices.loading import load_index_from_storage
        self.loaded_index = load_index_from_storage(self.storage_context)
        return self.loaded_index, self.node_dict





if __name__ == "__main__":

    from KB_function.DocumentLoader import DocumentLoader
    loader = DocumentLoader()
    docfile = "test.docx"
    text = loader.ReadDataToDocs(docfile, "text")

    indexstore = ContextIndex()
    indexstore.Construct(text,"text")
    indexstore.load()
    indexstore.AddFiles(text, "text2")

    #print(result)
    #indexstore = ContextIndex()
    indexstore.load()
    query = "how to partition documents"
    indexstore.Retriever(query, 2)



