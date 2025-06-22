from tinydb import TinyDB, Query
from typing import List, Dict, Optional
from uuid import UUID
import pandas as pd
from tinydb.storages import MemoryStorage

class InMemoryDB:
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the in-memory database
        
        Args:   
            db_path: Path to the database file. Use ":memory:" for in-memory only
        """

        self.db = TinyDB(db_path)
        self.sessions = self.db.table('sessions')



    def _create_session(self, session_id):

        self.sessions.insert({"session_id": session_id, 
                              "followup_count": 0,
                              "attribute_map": {},
                              "recommendations":[], 
                              "messages": [{"role": "assistant", "content": "I am here to help you with your apparel shopping needs. How May I Help You?"}]}) 


    def get_session(self, session_id: UUID):
        session = self.sessions.get(Query().session_id == session_id)
        if session is None:
            self._create_session(session_id)
        return self.sessions.get(Query().session_id == session_id)

    def delete_session(self, session_id: UUID):
        self.sessions.remove(Query().session_id == session_id)
    
    def update_chat_history(self, session_id: UUID, messages: List[Dict]):
        self.sessions.update({"messages": messages}, Query().session_id == session_id)

    def update_attribute_map(self, session_id: UUID, attribute_map: Dict):
        self.sessions.update({"attribute_map": attribute_map}, Query().session_id == session_id)

    def update_followup_count(self, session_id: UUID, followup_count: int):
        self.sessions.update({"followup_count": followup_count}, Query().session_id == session_id)
    
    def update_recommendations(self, session_id: UUID, recommendations: List):
        self.sessions.update({"recommendations": recommendations}, Query().session_id == session_id)

    def update_session(self, session_id: UUID, session: Dict):
        self.sessions.update(session, Query().session_id == session_id)

class SKUs:
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the in-memory database
        
        Args:
            db_path: Path to the database file. Use ":memory:" for in-memory only
        """
        self.db = TinyDB(db_path)
        self.skus = self.db.table('skus')

    def load_skus_from_excel(self, file_path: str):


        df = pd.read_excel(file_path)


        for index, row in df.iterrows():
            self.skus.insert({"id": row["id"], "name": row["name"], "category": row["category"], "available_sizes": row["available_sizes"], "fit": row["fit"], "fabric": row["fabric"], "sleeve_length": row["sleeve_length"], "color_or_print": row["color_or_print"], "occasion": row["occasion"], "neckline": row["neckline"], "length": row["length"], "pant_type": row["pant_type"], "price": row["price"]})

    