from llm_utils.prompts.prompts import PROMPTS
from llm_utils.models.base_llm import BaseLLM
from llm_utils.parameters import CONFIG

import json


class Router(BaseLLM):
    def __init__(self, model_name=CONFIG['base_model']):
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
            response_mime_type="application/json",
            max_output_tokens=128,
            log=False
        )

    def route_query(self, query: str):
        response = super().query(query)
        try:
            query_type = json.loads(response).get("query_type")
        except:
            try:
                query_type = json.loads(response.replace('```json', '').replace('```', '')).get("query_type")
            except:
                print(f"Router failed to identify query type. Defaulting to 'study'")
                query_type = "study"
        print(f"Router identified following system prompt: {query_type}")
        return query_type
