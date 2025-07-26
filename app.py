from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain.schema.runnable import RunnableLambda

from src.components.vector_database import Vector
from src.components.llm_model import LLMProcess
from src.config.config import SYSTEM_PROMPT

## Model part ##

# 1. loading local vector database
vector_process = Vector()

embedding_model = vector_process.load_embedding_model()

load_vector_store = vector_process.load_vector_store(
    embedding_model=embedding_model
)

# 2. create retriever
retriever = vector_process.create_retriever(
    vector_store=load_vector_store
)

# 3. LLM setup

llm = LLMProcess()

llm_model = llm.load_llm_model()

# 4. chain
store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# prompt
prompt = ChatPromptTemplate.from_messages([
    ('system' , SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', "{input}")
])

# create chain
qa_chain = create_stuff_documents_chain(llm = llm_model, prompt=prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)
wrapped_chain = rag_chain | RunnableLambda(lambda output: output["answer"])

chain_with_history = RunnableWithMessageHistory(
    wrapped_chain,
    get_by_session_id,
    input_messages_key="input",
    history_messages_key="chat_history"
)


# 5. API
app = FastAPI()

class ChatRequest(BaseModel):
    message : str
    
class ChatResponse(BaseModel):
    reply : str
    
    
@app.get("/")
async def home():    
    return {"message" : "Welcome To Chatbot API"}
    

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request : ChatRequest):
    
    user_query = request.message
    
    result = chain_with_history.invoke(
        {"input" : user_query},
        config = {
                "configurable": {"session_id": "mahadi"} # session id for unique user
            }
    )
    
    try:
        return JSONResponse(
            status_code=200,
            content={
                "reply" : result
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=200,
            content={str(e)}
        )
    
    