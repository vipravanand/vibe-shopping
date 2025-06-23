# Vibe-Shopping


## Repo Structure
- /app - FastAPI server for the app 
- app/main.py : Entry point that spins up the FastAPI server
- /data - Contains data files that include synthetic data ingested offline (vibe words in categories of fabric, fit, sustainable fashion, etc), SKU data for recommendation etc.  
- /prompts - Prompts for the app that power attribute extraction, vibe to attribute mapping and response generation
- /dev and /notebook are for development and testing purposes. 

## Orchestration 
- The agent is orchestrated by the AgentOrchestrationService class in app/services/chat_service.py
- The app is currently powered by a single agent - Apparel Search Agent
- It can be extended to include other agents for different use cases like Customer Support, Shipping, etc.

## Apparel Search Agent
- The app is powered by one main agent - Apparel Agent
- Apparel agents have 4 main tools:
    - product-engine: To recommend apparel
    - inform-engine: To inform the user about the apparel
    - purchase-engine: To purchase the apparel (not implemented, maybe handoff to a Payment Agent in a future implementation)
    - reject-engine: To reject the apparel that has been recommended


## Vibe to Attribute 
- The product engine tool is the central implementation in the current scope
- It is responsible for extracting vibe and attributes, mapping vibes to attributes, asking for followups (2 in number) and recommending apparel
- The app uses vibe to attribute mapping to infer the attributes from the user's query
- The app uses the following data files to map the vibe to attribute:
    - /data/fabric-vibe-mapping.csv
    - /data/fit-vibe-mapping.csv
    - /data/sustainable-fashion-vibe-mapping.csv
    - /data/occasion-vibe-mapping.csv
- These data files act as offline vocabulary on which exact and fuzzy matching followed by LLM-based inference is done to map the vibe to attribute

## Recommendation Engine
- The app uses the following data files to recommend apparel:
    - /data/apparel_data_v0.xlsx
- The SKUs that match the most number of attributes are recommended

## UI
- The chat UI can be accessed at: https://vibe-shopping-viprav.streamlit.app/
- The first request may take additional time as the backend is deployed in a cold start mode
- Every chat is mapped to the same session-id for memory purposes
- On pressing the clear button, the chat history is cleared and the session-id is reset to start a new session