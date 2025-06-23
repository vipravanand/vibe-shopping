from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional, Literal, Callable

from pydantic import BaseModel
from prompts.prompt_manager import PromptManager
from app.schema.structured_outputs.query_to_attribute import QueryToAttribute, VibeToAttribute
from utils.gpt_utils import GPTUtils
from app.database.in_memory_db import InMemoryDB
import pandas as pd
from pathlib import Path
from fuzzywuzzy import process


root = Path(__file__).parent.parent.parent



fabric_vibe_mapping = pd.read_csv(root / "data" / "fabric-vibe-mapping.csv")
fit_vibe_mapping = pd.read_csv(root / "data" / "fit-vibe-mapping.csv")
geo_zone_vibe_mapping = pd.read_csv(root / "data" / "geo-zone-vibe-mapping.csv")
occasion_vibe_mapping = pd.read_csv(root / "data" / "occasion-vibe-mapping.csv")
sustainability_vibe_mapping = pd.read_csv(root / "data" / "sustainability-vibe-mapping.csv")




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
    fn: Literal["product-engine", "inform-engine", "purchase-engine", "reject-engine"]

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
    

    def fuzzy_match(self, query: str, options: List[str]) -> str:
        best_match = process.extractOne(query, options)
        if best_match[1] > 80:
            return best_match[0]
        return None
    
    def return_response(self, response: str) -> str:
        return None
    

    def get_fabric_from_vibe(self, vibes: List[str]) -> str:
        fabric = []
        for vibe in vibes:
            #iterate over the rows , and return the fabric where required vibe matches teh set of vibes in Vive
            for index, row in fabric_vibe_mapping.iterrows():
                if vibe in row["Vibe"].split(",") or self.fuzzy_match(vibe, row["Vibe"].split(",")):
                    fabric.append(str(row["Fabric"]))
        return "\n".join(fabric)



    def get_fit_from_vibe(self, vibes: List[str]) -> str:
        fit = []
        for vibe in vibes:
            #iterate over the rows , and return the fit where required vibe matches teh set of vibes in Vive
            for index, row in fit_vibe_mapping.iterrows():
                if vibe in row["Vibe"].split(",") or self.fuzzy_match(vibe, row["Vibe"].split(",")):
                    fit.append(str(row["Fit"]))
        return "\n".join(fit)
    
    def get_geo_zone_from_vibe(self, vibes: List[str]) -> str:
        geo_zone = []
        for vibe in vibes:
            #iterate over the rows , and return the geo zone where required vibe matches teh set of vibes in Vive
            for index, row in geo_zone_vibe_mapping.iterrows():
                if vibe in row["Vibe"].split(",") or vibe in row["Zone"].split(",") or self.fuzzy_match(vibe, row["Vibe"].split(",")) or self.fuzzy_match(vibe, row["Zone"].split(",")):
                    geo_zone.append(str(row["Fabric & Fit Styles"]))
        return "\n".join(geo_zone)
    
    def get_occasion_from_vibe(self, vibes: List[str]) -> str:
        occasion = []
        for vibe in vibes:
            #iterate over the rows , and return the geo zone where required vibe matches teh set of vibes in Vive
            for index, row in occasion_vibe_mapping.iterrows():
                if vibe in row["Vibe"].split(",") or self.fuzzy_match(vibe, row["Vibe"].split(",")):
                    occasion.append(str(row["Occasion"]))
        return "\n".join(occasion)
    

    def get_sustainability_from_vibe(self, vibes: List[str]) -> str:
        sustainability = []
        for vibe in vibes:
            #iterate over the rows , and return the geo zone where required vibe matches teh set of vibes in Vive
            for index, row in sustainability_vibe_mapping.iterrows():
                if vibe in row["Vibe"].split(",") or vibe in row["Category"].split(","):
                    sustainability.append(str(row["Category"]))

        return "\n".join(sustainability)



    def normalise_for_vibe_to_attribute_mapping(self, attributes: Optional[List[str]]) -> str:
        if attributes is None:
            return []
        elif isinstance(attributes, list):
            return attributes
        



    def encrich_attribute_map(self):
        self.attribute_map.fit = self.normalise_for_vibe_to_attribute_mapping(self.attribute_map.fit) + self.normalise_for_vibe_to_attribute_mapping(self.vibe_to_attribute_map.fit)    
        self.attribute_map.fabric = self.normalise_for_vibe_to_attribute_mapping(self.attribute_map.fabric) + self.normalise_for_vibe_to_attribute_mapping(self.vibe_to_attribute_map.fabric)
        self.attribute_map.colour_or_print = self.normalise_for_vibe_to_attribute_mapping(self.attribute_map.colour_or_print) + self.normalise_for_vibe_to_attribute_mapping(self.vibe_to_attribute_map.colour_or_print)
        self.attribute_map.occasion = self.normalise_for_vibe_to_attribute_mapping(self.attribute_map.occasion) + self.normalise_for_vibe_to_attribute_mapping(self.vibe_to_attribute_map.occasion)




    def vibe_to_attibute_mapping(self) -> str:
        vibes = self.attribute_map.vibe
        if not vibes:
            return

        fabric = self.get_fabric_from_vibe(vibes)
        fit = self.get_fit_from_vibe(vibes)
        geo_zone = self.get_geo_zone_from_vibe(vibes)
        occasion = self.get_occasion_from_vibe(vibes)
        sustainability = self.get_sustainability_from_vibe(vibes)

        vibe_to_attribute_mapping_prompt = PromptManager.get_prompt("chat", "agent-apparel-tool-vibe-to-attribute_mapping", fit=fit, fabric=fabric, geo_zone=geo_zone, occasion=occasion, sustainability=sustainability, vibe=", ".join(vibes))
        vibe_to_attribute_mapping_prompt = vibe_to_attribute_mapping_prompt.replace("\n\n\n\n", "\n\n")
        system_prompt =     GPTUtils.build_system_prompt(vibe_to_attribute_mapping_prompt)
        messages = [system_prompt]
        self.vibe_to_attribute_map = GPTUtils.get_structured_output(messages, VibeToAttribute)
        self.session["messages"].append({"role": "user", "content": f"Based on the vibes {vibes}, following is the vibe to inferred attribute mapping: {self.vibe_to_attribute_map.model_dump()}"})
        self.db.update_chat_history(self.session_id, self.session["messages"])
        self.encrich_attribute_map()



    def extract_vibe_and_attributes(self) -> str:
        query_to_attribute_mapping_prompt = PromptManager.get_prompt("chat", "agent-apparel-tool-query-to-attribute_mapping")
        system_prompt = GPTUtils.build_system_prompt(query_to_attribute_mapping_prompt)
        messages = [system_prompt] + self.session["messages"]
        self.attribute_map = GPTUtils.get_structured_output(messages, QueryToAttribute)

        self.vibe_to_attibute_mapping() 

        self.session["messages"].append({"role": "user", "content": f"User Requirements:\n{self.attribute_map.model_dump() }"})
        self.db.update_chat_history(self.session_id, self.session["messages"])
        self.db.update_attribute_map(self.session_id, self.attribute_map.model_dump())


    def get_missing_data(self):
        missing_data = []
        for key, value in self.attribute_map.model_dump().items():
            if key == "vibe":
                continue
            if key == "price":
                if value is None or (value["min"] is None and value["max"] is None):
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
        


        
    def count_matches(self, row, filters):
        count = 0
        for size in filters["size"]:
            filters[size] = [True]


        for col, val in filters.items():
            if val and isinstance(val, list):
                val = set(val)
                for v in val: 
                    try:
                        if row[col] == v:
                            count += 1
                    except:
                        continue
                    
        return count
    

    def filter_by_price(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        if filters["price"] is None:
            return df
        if filters["price"]["min"] is None and filters["price"].max is None:
            return df
        if filters["price"].min is not None and filters["price"].max is not None:
            return df[df["price"] >= filters["price"].min and df["price"] <= filters["price"].max]
        
        if filters["price"]["min"] is not None and filters["price"]["max"] is None:
            return df[df["price"] >= filters["price"]["min"]]
        
        if filters["price"]["min"] is None and filters["price"]["max"] is not None:
            return df[df["price"] <= filters["price"]["max"]]
        
        return df

    
    def recommend_items(self) -> str:
        df = pd.read_excel(root / "data" / "Apparels_v0.xlsx")
        filters = self.attribute_map.model_dump()
        filters.pop("vibe")

        df["match_count"] = df.apply(lambda row: self.count_matches(row, filters), axis=1)
        df = df.sort_values(by="match_count", ascending=False)
        top_3_matches = "Mention that these are some items that match your requirements: " + df_price.head(2).to_string(index=False) + "Mention the reasons why this is a good match as per the attributes infeerred and vibes mentioned in the query."
        df_price = self.filter_by_price(df.copy(), filters)
        if len(df_price) == 0 and len(df) > 0:
            self.response = "Mention to the user: that While no items match the user's price range, here are some items that match your requirements: " + df.head(2).to_string(index=False) + "Mention the reasons why this is a good match as per the attributes infeerred and vibes mentioned in the query."
        elif len(df_price) > 0: 
            self.response = "Mentio to the user : Here are some items that match your requirements: " + df_price.head(2).to_string(index=False) + "Mention the reasons why this is a good match as per the attributes infeerred and vibes mentioned in the query."

        else:
            self.response = "Mention to the user : No items found that match your requirements. We wil update our stocks and get back to you soon."

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
            self.session["followup_count"] = 0
            self.response = "Ask the user if they can tell more about their requirements or preferences in detail for the item they are looking for."
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
        
