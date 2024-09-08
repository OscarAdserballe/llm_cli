import google.generativeai as genai
import os
from prompts import PROMPTS
from config_logger import get_logger
import json

class LLM:
    def __init__(self,
                 model_name: str="gemini-1.5-flash",
                 system_prompt: str=PROMPTS["default"],
                 route: bool=True,
                 log=True
            ):
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        self.system_prompt =system_prompt
        self.model_name = model_name
        self.generation_config = genai.GenerationConfig(
            max_output_tokens=8000
        )
        self.route = route
        self.log = log

        if self.log: self.logger = get_logger(__name__)

    def parse_shitty_response(self, response):
        return response.candidates[0].content.parts[0].text

    def query(self, query: str, context: str=""):
        if self.route:
            router = Router()
            type_of_query = router.route_query(query)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=PROMPTS[type_of_query]
            )
        else:
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.system_prompt
            )

        prompt = f"Query: {query}\n\n Context: {context}"
        response = self.model.generate_content(prompt)
        try:
            answer = response.text
        except:
            answer = self.parse_shitty_response(response)
        
        if self.log: self.logger.info(f"Query: {query}\n\n\nAnswer: {answer}\n\n\n\n\n\n")
        return answer

class Router(LLM):
    def __init__(self, model_name="gemini-1.5-flash"):
        self.system_prompt = f"""
        You are an agent receiving a query from a user. You must help classify the query and route it to the appropriate type of query based on the options available.
        You can route it to one of the following - use ONLY the options provided and match the keys exactly!
        Options:
        {PROMPTS.keys()}

        Example:
        <input>
        Can you help me code this?
        </input>
        <output>
        {{'query_type' : 'code'}}
        </output>

        If none of them fit at all, return {{'query_type' : 'study'}}

        ONLY RETURN IN JSON-FORMAT.  
        """
        super().__init__(
            model_name=model_name,
            system_prompt=self.system_prompt,
            route=False,
            log=False
        )
        self.generation_config = genai.GenerationConfig(
            max_output_tokens = 128,
            response_mime_type = "application/json"
        )

    def route_query(self, query: str):
        response = super().query(query)
        try:
            query_type = json.loads(response).get("query_type")
        except:
            query_type = json.loads(response.replace('```json', '').replace('```', '')).get("query_type")
        print(f"Router identified following system prompt: {query_type}")
        return query_type