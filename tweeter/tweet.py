try:
    from twitter import *
    from . import login
except:
    login = None

def send_tweet(text):
    try:
        twitter = Twitter(
            auth = OAuth(login["access_key"], login["access_secret"], login["consumer_key"], login["consumer_secret"]))

        results = twitter.statuses.update(status = text)
    except:
        print("Tweet not sent")

def send_tweet_with_image(text, image):
    try:
        twitter = Twitter(
            auth = OAuth(login["access_key"], login["access_secret"], login["consumer_key"], login["consumer_secret"]))

        with open(image, "rb") as imagefile:
            imagedata = imagefile.read()
        t_up = Twitter(domain='upload.twitter.com',
            auth = OAuth(login["access_key"], login["access_secret"], login["consumer_key"], login["consumer_secret"]))
        id_img = t_up.media.upload(media=imagedata)["media_id_string"]

        results = twitter.statuses.update(status=text, media_ids=id_img)

    except:
        print("Tweet not sent")
