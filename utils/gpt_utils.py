import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class GPTUtils:
    @staticmethod
    def get_structured_output( messages: List[Dict[str, Any]], response_model: BaseModel, model: str = "gpt-4o-mini", temperature: float = 0.0):
        response = client.responses.parse(
            model=model,
            input=messages,
            text_format=response_model, 
            temperature=temperature,
        )
        print(response.output_parsed)
        return response.output_parsed
    
    @staticmethod
    def get_response(messages: List[Dict[str, Any]], model: str = "gpt-4o-mini", temperature: float = 0.0):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
 
    @staticmethod
    def build_system_prompt(prompt: str):
        return {"role": "system", "content": prompt}
    

    @staticmethod
    def build_user_prompt(prompt: str):
        return {"role": "user", "content": prompt}
    

    @staticmethod
    def build_tool_prompt(prompt: str):
        return {"role": "tool", "content": prompt}



    @staticmethod
    def build_assistant_prompt(prompt: str):
        return {"role": "assistant", "content": prompt}
    

    @staticmethod
    def add_context(messages: List[Dict[str, Any]], context):
        messages.append(context)
        return messages





    

    
