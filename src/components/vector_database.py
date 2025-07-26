from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


from src.config.config import HUGGINGFACEHUB_API_TOKEN, EMBEDDING_REPO_ID, DB_FAISS_PATH
from src.utils.logger import logger
from src.utils.custom_exception import CustomException

logger = logger(__name__)

class Vector:
    
    def __init__(self):
        pass
    
    # laod embedding model
    def load_embedding_model(self):
        try:
            logger.info("Loading Embedding Model..........")
            model = HuggingFaceEmbeddings(model_name = EMBEDDING_REPO_ID)  
            logger.info("Embedding Model loaded Successfully")
            
            return model
        except Exception as e:
            error = CustomException("Error occurred while loading model",e)
            logger.error(str(error))
    
    # Create vector store
    def create_vector_store(self, chunks, embedding_model):
        try:
            logger.info("Generating VectorStore........")
            vector_store = FAISS.from_documents(
                documents=chunks,
                embedding=embedding_model
            )
            
            logger.info("Saving VectorStore")
            vector_store.save_local(DB_FAISS_PATH)
    
            return vector_store
        
        except Exception as e:
            error = CustomException("Failed To create vectorStore", e)
            logger.error(str(error))
            
    
    # load vector store
    def load_vector_store(self, embedding_model):
        try:
            logger.info("Loading VectorStore......")
            
            load_vector = FAISS.load_local(
                DB_FAISS_PATH,
                embedding_model,
                allow_dangerous_deserialization=True
            )
            
            logger.info("Loaded VectorStore Successfully")
            
            return load_vector
        except Exception as e:
            error = CustomException("Failed To load vector DB")
            logger.error(error)
            
            
        # create retriever
    def create_retriever(self,vector_store):
        try:
            logger.info("Creating retriever...........")
            retriever = vector_store.as_retriever(
                            search_type="similarity",
                            search_kwargs={
                                "k": 10,                      
                                "score_threshold": 0.5,      
                                "include_metadata": True,    
                                "fetch_k": 20               
                            }
                        )    
            return retriever
        except Exception as e:
            error = CustomException("Failed to create retriever",e)
            logger.error(str(error))
            