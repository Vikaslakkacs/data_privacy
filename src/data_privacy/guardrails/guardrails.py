import os
from dotenv import load_dotenv
### importing guardrail packges
from nemoguardrails import RailsConfig, LLMRails

class guardrails():
    def __init__(self, config_path):
        self.config_path= config_path
    
    def initiate_rails(self):
        config= RailsConfig.from_path(self.config_path)
        #print(self.config_path)
        rails= LLMRails(config=config)
        
        return rails
        