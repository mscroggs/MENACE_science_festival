from twitter import *

def send_tweet(text):
    config = {}
    execfile("config.py", config)

    twitter = Twitter(
        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

    results = twitter.statuses.update(status = text)
