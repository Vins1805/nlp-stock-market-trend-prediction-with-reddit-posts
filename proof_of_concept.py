from tools.tools import Reddit
from tools.translations import IO, POST_TYPE
import pandas as pd

# https://www.reddit.com/dev/api/
params = {
    "limit": "100",
    }

r = Reddit(params)

url = IO["BASE"] + IO["SUBR"]["STOCKMARKET"] + IO["LIST"]["HOT"]
print(url)

#print(r.pretty(r.open(url)))
#print(r.open(url))


df = pd.DataFrame()

for post in r.open(url)["data"]["children"]:
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
        "created": post["data"]["created"],
        "created_utc": post["data"]["created_utc"],
        "kind": POST_TYPE[post["kind"]],
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

print(df)
print(IO["BASE"] + df.loc[0].permalink)
print(r.pretty(r.open(IO["BASE"] + df.loc[0].permalink)))

#0 = post
#1..n = comments
# data -> children
#name
#body
#archived
#controversiality
#created
#created_utc
#depth
#downs
#link_id
#parent_id
#permalink
#kind
#replies <- recursion
