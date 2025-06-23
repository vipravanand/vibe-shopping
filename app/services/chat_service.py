from typing import List, Optional, Literal, Any, Dict
from app.schema.requests.chat import ChatRequest
from prompts.prompt_manager import PromptManager
from utils.gpt_utils import GPTUtils
from pydantic import BaseModel, Field
from app.agents.agents import ApparelSearchAgent, Agent
from app.database.in_memory_db import InMemoryDB


master_agents_list = [ApparelSearchAgent]





class SubQuery(BaseModel):
    """
    Router is to be decomposed into a list of synonyms of the key words, the vibe, and the attributes for the search.
    The reasoning is used to explain 
    """
    query: str 
    agents: Literal["apparel-search-agent"]
    reasoning: str


class Router(BaseModel):
    """
    Router is to be decomposed into a list of synonyms of the key words, the vibe, and the attributes for the search.
    The reasoning is used to explain    
    """
    sub_queries: Optional[List[SubQuery]] = Field(default=None)



class ChatSession(BaseModel):

    request: Optional[ChatRequest] = None
    router: Optional[Router] = None
    tool_results: Optional[List[Any]] = None
    follow_up: Optional[str] = None
    response: Optional[str] = None
    session_id: Optional[List[Dict]] = None


class AgentOrchestrationService:
    def __init__(self, request: ChatRequest):
        self.request = request
        self.db = InMemoryDB()
        self.session_id = request.session_id
        self.session = self.db.get_session(self.session_id)

        self.agents = [agent(self.db, self.session_id) for agent in master_agents_list]
        self.agent_responses: List[Any] = []
        self.agent_definitions = {agent.name: agent.description for agent in master_agents_list}
        self.agent_mapping: Dict[str, Agent] = {agent.name: agent(self.db, self.session_id) for agent in master_agents_list}
        self.session["messages"].append({"role": "user", "content": self.request.message})
        self.db.update_chat_history(self.session_id, self.session["messages"])


    def chat(self) -> str:

        self.get_query_plan()
        self.call_agents()
        return self.final_response()


    def get_query_plan(self):
        agents_definitions_str = "\n".join([f"{agent.name}: {agent.description}" for agent in self.agents])
        routing_system_prompt= PromptManager.get_prompt("chat", "orchestrator-query-planner", agents_definitions= agents_definitions_str)
        system_prompt = GPTUtils.build_system_prompt(routing_system_prompt)
        messages = [system_prompt] + self.session["messages"]
        self.query_plan = GPTUtils.get_structured_output(messages, response_model=Router)
    

    def add_agent_responses_to_llm_context(self):
        instructions = ""
        for agent_response in self.agent_responses:
            instructions = f"{agent_response}\n"
        self.session["messages"].append({"role": "user", "content": instructions})
    

    def final_response(self):
        self.session = self.db.get_session(self.session_id)
        self.add_agent_responses_to_llm_context()
        
        response_prompt = PromptManager.get_prompt("chat", "orchestrator-final-response-generation")
        system_prompt = GPTUtils.build_system_prompt(response_prompt)
        messages = [system_prompt] + self.session["messages"]
        response = GPTUtils.get_response(messages)

        self.session["messages"].append({"role": "assistant", "content": response})
        self.db.update_chat_history(self.session_id, self.session["messages"])

        return response
    
    
    def get_agent_response(self, agent) -> Any:
        return self.agent_mapping[agent].execute()
    
    
    
    def call_agents(self):
        agents = {subquery.agents for subquery in self.query_plan.sub_queries}
        for agent in agents:
            agent_results = self.get_agent_response(agent)
            self.agent_responses.append(agent_results)




        


    # async def query_engine(self, request: ChatRequest))
    #     query_engine_prompt = PromptManager.get_prompt("chat", "query_engine")
    #     system_prompt = GPTUtils.build_system_prompt(query_engine_prompt)
    #     messages = [system_prompt] + request.messages
    #     response = GPTUtils.get_structured_output(messages)
    #     return response
    





