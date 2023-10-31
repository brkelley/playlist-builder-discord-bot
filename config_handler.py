import json

file_location = 'bot_config.json'

class ConfigHandler:
    def __init__(self):
        self.emoji = ''
        self.role = ''
        with open(file_location, 'r') as f:
            data = json.load(f)
            
            if 'emoji' in data:
                self.emoji = data['emoji']
            if 'role' in data:
                self.role = data['role']
    
    def findMissingPieces(self):
        missingPieces = {
            'emoji': True,
            'role': True
        }
        if self.emoji != '':
            missingPieces['emoji'] = False
        if self.role != '':
            missingPieces['role'] = False
        
        return missingPieces

    def setEmoji(self, emoji):
        self.emoji = emoji
        self.writeToConfig()

    def setRole(self, role):
        self.role = role
        self.writeToConfig()

    def writeToConfig(self):
        with open(file_location, 'w') as json_file:
            config_dict = {
                'emoji': self.emoji,
                'role': self.role
            }
            json.dump(config_dict, json_file)
