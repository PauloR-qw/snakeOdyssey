import json
from typing import Dict

class Data:

    @staticmethod
    def getConfigs ():

        with open('./config.json') as configFile:
            return json.load(configFile)
    
    @staticmethod
    def setConfigs (newConfig: Dict):

        with open('./config.json', 'w') as configFile:
            json.dump(newConfig, configFile)

    @staticmethod
    def getTrans ():

        lang = Data.getConfigs()['language']
        with open(f'./data/lang/{lang}.json') as langFile:
            return json.load(langFile)