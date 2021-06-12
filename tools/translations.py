import os

IO = {
    "BASE": "https://oauth.reddit.com/",
    "SUBR": {
        "STOCKMARKET": "r/StockMarket/",
        },
    "LIST": {
        "HOT": "hot/",
        "NEW": "new/",
        "BEST": "best/",
        "RISING": "rising/",
        "TOP": "top/",
        "CONTROVERSIAL": "controversial/",
        },
    "OUTPUT": {
        "THREADS": os.getcwd() + os.sep + "data" + os.sep
        }
    }

REDDIT_TYPE = {
    "t1": "Comment",
    "t2": "Account",
    "t3": "Link",
    "t4": "Message",
    "t5": "Subreddit",
    "t6": "Award",
    }
