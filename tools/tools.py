import requests
import json

# https://www.reddit.com/prefs/apps
from tools.config import api, reddit_user



class Reddit:
    def __init__(self, params = dict()):
        if isinstance(params, dict):
            self.params = params
        else:
            self.params = dict()
        
        auth = requests.auth.HTTPBasicAuth(*api.values())

        login_data = reddit_user
        login_data["grant_type"] = "client_credentials"

        self.headers = {"User-Agent": "NLP-Script"}

        res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=login_data,
            headers=self.headers
            )

        TOKEN = res.json()["access_token"]

        self.headers["Authorization"] = f"bearer {TOKEN}"

        
    def open(self, url):
        return requests.get(url, headers=self.headers, params=self.params).json()


    @staticmethod
    def pretty(input_json: dict) -> str:
        return json.dumps(input_json, indent=4, sort_keys=True)
