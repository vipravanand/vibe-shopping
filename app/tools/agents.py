from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Literal, Callable

from pydantic import BaseModel
from prompts.prompt_manager import PromptManager
from app.schema.structured_outputs.query_to_attribute import QueryToAttribute
from utils.gpt_utils import GPTUtils
from app.database.in_memory_db import InMemoryDB

class AgentResponse(BaseModel):
    instructions: str
    metadata: Optional[Dict[str, Any]] = None

class Agent(ABC):
    """
    Agent is a class that represents an agent that can be used to execute a query.
    """

    name: str
    description: str
    response: AgentResponse


    def __init__(self, db: InMemoryDB, session_id: str):
        self.db = db
        self.session_id = session_id

    @abstractmethod
    def execute(self) -> str:
        pass





class SearchItemsAgent(Agent):
    """
    SearchItemsAgent is an agent that can be used to search for any fashion item.
    """
    name: str = "search-items"
    description: str = "When the user asks for a specific item of fashion like clothing, shoes, accessories, etc., you can use this tool to search for it."\
                        "The user may privide a specific item or general description of the item of clothing."


    @abstractmethod
    def execute(self, chat_history: List[Dict[str, Any]]) -> str:
        pass

    @abstractmethod
    def extract_vibe_and_attributes(self, chat_history: List[Dict[str, Any]]) -> str:
        pass

    @abstractmethod
    def return_response(self, response: str) -> str:
        pass

    @abstractmethod
    def next_step(self, chat_history: List[Dict[str, Any]]) -> str:
        pass

    @abstractmethod
    def make_item_recommendations(self, chat_history: List[Dict[str, Any]]) -> str:
        pass


    @abstractmethod
    def followup_engine(self, chat_history: List[Dict[str, Any]]) -> str:
        pass

    @abstractmethod
    def ask_llm_for_next_step(self, chat_history: List[Dict[str, Any]]) -> str:
        pass




class ApparelTools(BaseModel):
    fn: Literal["product-engine", "inform-engine", "purchase-engine", "reject-engine", "fall-back"]

class ApparelSearchAgent(Agent):
    """
    ßApparelSearchAgent is an agent that can be used to search for apparel.
    """
    name: str = "apparel-search-agent"
    description: str = "When the user asks for a specific item of clothing, you can use this agent to search for it."\
                        "The user may mention a specific item of clothing, or a general description of the item of clothing."

    def fn_mappimg(self, fn:str) -> Callable:
        mapping = {
            "product-engine": self.product_engine,
            "inform-engine": self.inform_engine,
            "purchase-engine": self.purchase_engine,
            "reject-engine": self.reject_engine
        }
        return mapping[fn]
    
    def return_response(self, response: str) -> str:
        return None


    def extract_vibe_and_attributes(self) -> str:
        query_to_attribute_mapping_prompt = PromptManager.get_prompt("chat", "agent-apparel-tool-query-to-attribute_mapping")
        system_prompt = GPTUtils.build_system_prompt(query_to_attribute_mapping_prompt)
        messages = [system_prompt] + self.session["messages"]
        self.attribute_map = GPTUtils.get_structured_output(messages, QueryToAttribute)
        self.session["messages"].append({"role": "user", "content": f"User Requirements:\n{self.attribute_map.model_dump()}"})
        self.db.update_chat_history(self.session_id, self.session["messages"])
        self.db.update_attribute_map(self.session_id, self.attribute_map.model_dump())


    def get_missing_data(self):
        missing_data = []
        for key, value in self.attribute_map.model_dump().items():
            if key == "price":
                if value is None or [value.min is None and value.max is None]:
                    missing_data.append(key)
            elif value is None:
                missing_data.append(key)
            elif isinstance(value, list) and len(value) == 0:
                missing_data.append(key)
        return missing_data

    def followup(self):
        followup_count = self.session["followup_count"]
        attribute_map = self.db.get_session(self.session_id)["attribute_map"]   
        missing_data = self.get_missing_data()

        if len(missing_data) > 0 and followup_count < 2:
            self.response = "Following attributes are missing: " + ", ".join(missing_data) + ". Please ask a followup to ask any 1 or 2 most critical attributes for recoomendation. Please do  not ask for all the attributes at once. Please do not ask for the same attribute again. Please do not add providr any suggestions , just ask for the missing attributes."
            self.session["followup_count"] = followup_count + 1
            self.db.update_followup_count(self.session_id, self.session["followup_count"])
            return True
        

    def recommend_items(self) -> str:
        self.response = "Recommending a an item with a creative name matchinh user requirements"

    def recommend(self) -> str:
        if not self.followup():
            self.recommend_items()


    def not_implemented(self) -> str:
        self.response = "Inform the user that currently we do not have the capability to do this. We will updated you as soon as we have the capability to do this."
        
    def product_engine(self) -> str:
        self.extract_vibe_and_attributes()
        self.missing_data = self.get_missing_data()
        self.recommend()

    def inform_engine(self) -> str:
        if len(self.session["recommendations"]) > 0:
            self.response = f"Share the information asked the user  based on item recommended: {self.sessiom["recommendations"][-1]}"
        else:
            self.product_engine()
    
    def purchase_engine(self) -> str:
        self.not_implemented()
    
    
    def reject_engine(self) -> str:
        if len(self.session["recommendations"]) > 0:
            self.session["recommendations"] = []
            self.response = "Ask the user if they can tell more about their requirements or preferences for the item they are looking for."
        else:
            self.product_engine()
    
    def fall_back(self) -> str:
        self.not_implemented()

    def get_tools(self) -> str:
        template = PromptManager.get_prompt("chat", "agent-apparel")
        system_prompt = GPTUtils.build_system_prompt(template)
        messages = [system_prompt] + self.session["messages"] + [{"role": "assistant", "content": "I am here to help you with your apparel shopping needs. How May I Help You?"}]
        tools: ApparelTools = GPTUtils.get_structured_output(messages, response_model = ApparelTools)
        return tools.fn
    
    def execute(self) -> str:
        self.session = self.db.get_session(self.session_id)
        self.fn_mappimg(self.get_tools())()
        return self.response
        
