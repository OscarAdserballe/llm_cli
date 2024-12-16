from llm_utils.models.base_llm import BaseLLM
from llm_utils.models.router import Router
from llm_utils.prompts.prompts import PROMPTS
from llm_utils.parameters import CONFIG

from config_logger import (
    LOG_DELIMITER,
    LOG_FILE
)

import os
import google.generativeai as genai

class LLM(BaseLLM):
    def __init__(
            self,
            model_name: str=CONFIG['base_model'],
            system_prompt: str=PROMPTS["default"],
            route: bool=False,
            log=True,
            use_chat_history: bool=True,
            temperature: float=0.5
        ):

        super().__init__(
            model_name=model_name,
            system_prompt=system_prompt,
            temperature=temperature,
            log=log
        )
        self.use_chat_history = use_chat_history
        self.route = route
    
    def fetch_chat_history(self, last_n=5):
        days_log_file = LOG_FILE

        if os.path.exists(days_log_file):
            with open(days_log_file, "r") as f:
                raw_log = f.read()

        chat_history = raw_log.split(LOG_DELIMITER)
        return chat_history[-last_n:]
    
    def query(self, query: str, context: str="", images: list=[]):
        if self.route:
            router = Router()
            type_of_query = router.route_query(query)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=PROMPTS[type_of_query]
            )

        if self.use_chat_history:
            context += f"""
            Chat History:

            {self.fetch_chat_history()}
            """
        
        response = super().query(query, context, images)
        return response

