from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.settings import Settings
from llama_index.core.node_parser import SentenceSplitter


from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore

from llama_index.core.retrievers import VectorIndexRetriever

import faiss
from llama_index.vector_stores.faiss import FaissVectorStore



from KB_function.EmbeddingModel import EmbeddingModel

import kb_configs
import configs


class ContextIndex():
    def __init__(self):
        dimension = configs.embedding_vec_len
        self.faiss_index = faiss.IndexFlatIP(dimension)
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
        # embedding
        embed = EmbeddingModel()
        embed_model = embed.get_model()
        Settings.llm = None
        Settings.embed_model=embed_model

        from llama_index.core.indices.loading import load_index_from_storage
        self.loaded_index = load_index_from_storage(self.storage_context)

    def Construct(self, docs, filename):
        # embedding
        embed = EmbeddingModel()
        embed_model = embed.get_model()
        Settings.llm = None
        Settings.embed_model = embed_model
        #nodes
        simple_node_parser = SentenceSplitter.from_defaults(chunk_size=kb_configs.chunk_size_small,
                                                          chunk_overlap=kb_configs.chunk_overlap_small)
        simple_nodes = simple_node_parser.get_nodes_from_documents(docs)
        loaded_index = VectorStoreIndex(simple_nodes,
                                        storage_context=self.storage_context)
        loaded_index.storage_context.persist(kb_configs.path_kb)

    def AddFiles(self, docs, filename):
        # base nodes
        # nodes
        simple_node_parser = SentenceSplitter.from_defaults(chunk_size=kb_configs.chunk_size_small,
                                                            chunk_overlap=kb_configs.chunk_overlap_small)
        simple_nodes = simple_node_parser.get_nodes_from_documents(docs)

        self.loaded_index.insert_nodes(simple_nodes,
                                       storage_context=self.storage_context)
        self.loaded_index.storage_context.persist(kb_configs.path_kb)


    def Retriever(self, query, topk):
        retriever_chunk = VectorIndexRetriever(
            index=self.loaded_index,
            similarity_top_k=topk,
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
        # embedding
        embed = EmbeddingModel()
        embed_model = embed.get_model()
        Settings.llm = llm
        Settings.embed_model = embed_model

        from llama_index.core.indices.loading import load_index_from_storage
        self.loaded_index = load_index_from_storage(self.storage_context)
        return self.loaded_index


if __name__ == "__main__":
    from KB_function.DocumentLoader import DocumentLoader

    loader = DocumentLoader()
    docfile = "test.docx"
    text = loader.ReadDataToDocs(docfile, "text")

    indexstore = ContextIndex()
    indexstore.Construct(text, "text")
    indexstore.load()
    indexstore.AddFiles(text, "text2")

    # print(result)
    # indexstore = ContextIndex()
    indexstore.load()
    query = "how to partition documents"
    indexstore.Retriever(query, 2)
