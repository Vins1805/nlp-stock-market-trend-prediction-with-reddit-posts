from tools.tools import Reddit

r = Reddit()

print(r.pretty(r.open("https://oauth.reddit.com/api/v1/me")))
