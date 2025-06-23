from abc import ABC, abstractmethod
from typing import List, Any, Dict
from prompts.prompt_manager import PromptManager
from app.schema.structured_outputs.query_to_attribute import QueryToAttribute
from utils.gpt_utils import GPTUtils
from app.database.in_memory_db import InMemoryDB


class Tool(ABC):
    """
    Tool is a class that represents a tool that can be used to execute a query.
    """

    name: str
    description: str


    def __init__(self, db: InMemoryDB, session_id: str):
        self.db = db
        self.session_id = session_id

    @abstractmethod
    def execute(self, chat_history: List[Dict[str, Any]]) -> str:
        pass



class SearchItemsTool(Tool):
    """
    SearchItemsTool is a tool that can be used to search for any fashion item.
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




class ApparelSearchAgent(Tool):
    """
    ApparelSearchTool is a tool that can be used to search for apparel.
    """
    name: str = "apparel-search-agent"
    description: str = "When the user asks for a specific item of clothing, you can use this tool to search for it."\
                        "The user may mention a specific item of clothing, or a general description of the item of clothing."
    
    def return_response(self, response: str) -> str:
        return None


    def extract_vibe_and_attributes(self, chat_history: List[Dict[str, Any]]) -> str:
        query_to_attribute_mapping_prompt = PromptManager.get_prompt("chat", "query_to_attribute_mapping")
        system_prompt = GPTUtils.build_system_prompt(query_to_attribute_mapping_prompt)
        messages = [system_prompt] + chat_history
        response = GPTUtils.get_structured_output(messages, QueryToAttribute)
        chat_history.append({"role": "user", "content": f"User Requirements:\n{response.model_dump()}"})
        self.db.update_chat_history(self.session_id, chat_history)
        self.db.update_attribute_map(self.session_id, response.model_dump())


    def missing_data(self, attribute_map: Dict):
        missing_data = []
        for key, value in attribute_map.items():
            if key == "vibe":
                continue
            if key == "price":
                if value is None or [value.min is None and value.max is None]:
                    missing_data.append(key)
            elif value is None:
                missing_data.append(key)
            elif isinstance(value, list) and len(value) == 0:
                missing_data.append(key)
        return missing_data
    


    def followup_engine(self):
        followup_count = self.session["followup_count"]
        attribute_map = self.db.get_session(self.session_id)["attribute_map"]   
        missing_data = self.missing_data(attribute_map)

        if len(missing_data) > 0 and followup_count < 2:
            instruction = {"role": "user", 
                           "content": "Following attributes are missing: " + ", ".join(missing_data) + ". Please ask a followup to ask any 1 or 2 most critical attributes for recoomendation. Please do  not ask for all the attributes at once. Please do not ask for the same attribute again."}
            self.session["messages"].append(instruction)
            self.db.update_chat_history(self.session_id, self.session["messages"])
            self.session["followup_count"] = followup_count + 1
            self.db.update_followup_count(self.session_id, self.session["followup_count"])



    def determine_next_step(self, chat_history: List[Dict[str, Any]]) -> str:
        pass
    

    def execute(self, chat_history: List[Dict[str, Any]]) -> str:

        system_prompt = PromptManager.get_prompt("chat", "apparel_search_agent")

        query_to_attribute = self.extract_vibe_and_attributes(chat_history)


        

