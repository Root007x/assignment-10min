from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint, ChatHuggingFace

from src.config.config import HUGGINGFACE_REPO_ID, HUGGINGFACEHUB_API_TOKEN
from src.utils.logger import logger
from src.utils.custom_exception import CustomException


logger = logger(__name__)



class LLMProcess:
    def __init__(self):
        pass
    
    # LLM model
    def load_llm_model(self):
        # setup endpoint
        try:
            logger.info("Loading LLM Model..........")
            llm_endpoint = HuggingFaceEndpoint(
                                repo_id= HUGGINGFACE_REPO_ID
                            )
            model = ChatHuggingFace(llm = llm_endpoint)
            logger.info("LLM Loaded Successfully")
            return model
        except Exception as e:
            error = CustomException("Failed To load LLM model",e)
            logger.error(str(error))
            
    
    