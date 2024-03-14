import json
import os

def load_config(config_file=os.path.abspath('config.json')):
    file_path = os.path.join(os.path.dirname(__file__), config_file)
    with open(file_path) as f:
        return json.load(f)

def load_token(token=os.path.abspath('token/token.json')):
    with open(token) as f:
        token_data = json.load(f)
        return token_data.get('token')