import json
import requests
from datetime import datetime, timedelta
import os
import base64

class TokenManager:
    def __init__(self, config_file=os.path.abspath('config.json'), token_file=os.path.abspath('token/token.json')):
        self.config_file = config_file
        self.token_file = token_file
        self.load_token_from_file()
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file) as f:
                config_data = json.load(f)
                self.config_data = config_data.get('backend', {})  # Extract backend data
        else:
            self.config_data = {
                "username": "admin",
                "password": "hashtopolis",
                "backend_url": "http://localhost:8080/api/v2"
            }
            self.save_config_to_file()  # Save default config if file doesn't exist

    def load_token_from_file(self):
        if os.path.exists(self.token_file):
            with open(self.token_file) as f:
                self.token_data = json.load(f)
        else:
            self.token_data = {"token": None, "expires": None}
            self.save_token_to_file()  # Save initial token data if file doesn't exist

    def save_config_to_file(self):
        with open(self.config_file, 'w') as f:
            json.dump({"backend": self.config_data}, f)  # Save only the backend part

    def save_token_to_file(self):
        with open(self.token_file, 'w') as f:
            json.dump(self.token_data, f)

    def get_token(self):
        if self.token_data['token'] is None or self.is_token_expired():
            self.refresh_token()
        return self.token_data['token']

    def is_token_expired(self):
        if self.token_data['expires'] is not None:
            expiration_time = datetime.fromisoformat(self.token_data['expires'])
            return expiration_time < datetime.utcnow()
        return True

    def refresh_token(self):
        credentials = f"{self.config_data['username']}:{self.config_data['password']}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode() #base64 encode credentials
        url = self.config_data['backend_url'] + '/auth/token'  #Auth path
        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            token_data = response.json()
            token_data['expires'] = (datetime.utcnow() + timedelta(seconds=3600)).isoformat()
            self.token_data = token_data
            self.save_token_to_file()
            print("Token refreshed successfully.")
        else:
            print(f"Failed to refresh token. Status code: {response.status_code}, Reason: {response.reason}")

if __name__ == "__main__":
    token_manager = TokenManager()
    token = token_manager.get_token()
    print("Token:", token)
