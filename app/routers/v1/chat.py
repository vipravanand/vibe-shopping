from fastapi import APIRouter
from app.schema.requests.chat import ChatRequest
from app.services.chat_service import AgentOrchestrationService
from fastapi.responses import JSONResponse



router = APIRouter(
    prefix="/v1/agent",
    tags=["agent"],
)



@router.post("/chat")
def chat(chat_request: ChatRequest) -> JSONResponse:
    chat_service: AgentOrchestrationService = AgentOrchestrationService(chat_request)
    response:str =  chat_service.chat()
    return JSONResponse(content={"response": response})

