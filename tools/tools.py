import requests
import json
import pandas as pd
from datetime import datetime as dt
from tools.translations import REDDIT_TYPE, IO
import os

# https://www.reddit.com/prefs/apps
from tools.config import api, reddit_user



class Reddit:
    def __init__(self):       
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

    @property
    def params(self):
        params = {
            "limit": "100",
            }
        return params.copy()
        

    def pretty(self, input_json: dict) -> str:
        return json.dumps(input_json, indent=4, sort_keys=True)

        
    def open(self, url, params=None):
        if not params:
            params = self.params
        return requests.get(url, headers=self.headers, params=params).json()


    def get_threads(self, url, params=None):
        if not isinstance(url, str):
            raise ValueError

        df = pd.DataFrame()

        for post in self.open(url, params)["data"]["children"]:
            award_names = {
                f"award_name{i}": award["name"]
                for i, award in enumerate(post["data"]["all_awardings"])
                }
            
            award_counts = {
                f"award_count{i}": award["count"]
                for i, award in enumerate(post["data"]["all_awardings"])
                }
            
            df = df.append({
                "id": post["kind"] + "_"+ post["data"]["id"],
                "created_at": dt.utcfromtimestamp(post["data"]["created_utc"]),
                "kind": REDDIT_TYPE[post["kind"]],
                "subreddit": post["data"]["subreddit"],
                "title": post["data"]["title"],
                "permalink": post["data"]["permalink"],
                "num_comments": post["data"]["num_comments"],
                "score": post["data"]["score"],
                "ups": post["data"]["ups"],
                "downs": post["data"]["downs"],
                "upvote_ratio": post["data"]["upvote_ratio"],
                "selftext": post["data"]["selftext"],
                "total_awards_received": post["data"]["total_awards_received"],
                **award_names,
                **award_counts
                }, ignore_index=True)
        return df

    def get_comments(self, data, params=None):
        if not data:
            return None
        
        if isinstance(data, str):
            data = self.open(data, params)[1]

        df = pd.DataFrame()
        
        for comment in data["data"]["children"]:
            award_names = {
                f"award_name{i}": award["name"]
                for i, award in enumerate(comment["data"]["all_awardings"])
                }
            
            award_counts = {
                f"award_count{i}": award["count"]
                for i, award in enumerate(comment["data"]["all_awardings"])
                }
            
            df = df.append({
                "id": comment["kind"] + "_"+ comment["data"]["id"],
                "created_at": dt.utcfromtimestamp(comment["data"]["created_utc"]),
                "name":  comment["data"]["name"],
                "archived":  comment["data"]["archived"],
                "controversiality":  comment["data"]["controversiality"],
                "depth":  comment["data"]["depth"],
                "kind": REDDIT_TYPE[comment["kind"]],
                "subreddit": comment["data"]["subreddit"],
                "body": comment["data"]["body"],
                "link_id": comment["data"]["link_id"],
                "parent_id": comment["data"]["parent_id"],
                "permalink": comment["data"]["permalink"],
                "score": comment["data"]["score"],
                "ups": comment["data"]["ups"],
                "downs": comment["data"]["downs"],
                "total_awards_received": comment["data"]["total_awards_received"],
                **award_names,
                **award_counts
                }, ignore_index=True)

            df = pd.concat([df, self.get_comments(comment["data"]["replies"])])
            
        return df


    def bulk_store_threads(self, url, n=1):
        df = pd.DataFrame()
        
        for i in range(n):
            params = self.params
            if i > 0:
                params["after"] = df.id.iloc[-1]
            df = pd.concat([df, self.get_threads(url, params)], sort=False)
            
        df = df.sort_values("created_at")
        df["created_at"] = df.created_at.apply(lambda date: date.date())
        df.reset_index(inplace=True)
        
        filepath = IO["OUTPUT"]["THREADS"] + f"{df.subreddit.iloc[0]}\\"

        for date, sub_df in df.groupby("created_at"):
            fp = filepath + f"{date}.pd"
            df.to_pickle(fp)
            

    def load_threads(self): # todo add parser to load specifc dates
        filepath = IO["OUTPUT"]["THREADS"]
        files = os.listdir(filepath)

        cols_to_select = ["selftext", "title"]
        df = pd.DataFrame()
        
        for file in files:
            df2 = pd.read_pickle(os.path.join(filepath, file))
            df = pd.concat([df, df2], sort=False)

        return df
            
            
    
