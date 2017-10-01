from twitter import *
from . import login

def send_tweet(text):

    twitter = Twitter(
        auth = OAuth(login["access_key"], login["access_secret"], login["consumer_key"], login["consumer_secret"]))

    results = twitter.statuses.update(status = text)
