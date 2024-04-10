import os
from dotenv import load_dotenv
### importing guardrail packges
from nemoguardrails import RailsConfig, LLMRails
import asyncio 
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class guardrails():
    def __init__(self, config_path):
        self.config_path= config_path
    
    def initiate_rails(self):
        config= RailsConfig.from_path(self.config_path)
        #print(self.config_path)
        rails= LLMRails(config=config)
        
        return rails
        