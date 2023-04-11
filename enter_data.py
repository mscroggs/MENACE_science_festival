#!/usr/bin/env python
import data_collector
import sys

if "resume" in sys.argv:
    c = data_collector.Collector(
        "data-dump/resume.json",
        where="the @IMAMaths Festival at @SHUMaths",
        hashtag="#MENACE #IMAFest22")
else:
    c = data_collector.Collector(
        where="the @IMAMaths Festival at @SHUMaths",
        hashtag="#MENACE #IMAFest22")

if "test" in sys.argv:
    c.TWEETING = False

try:
    c.start()
except KeyboardInterrupt:
    print("Is is the end of the day? y/n ")
    end = c.prompt(["y","n"])
    if end=="y":
        c.save("data-dump/final.json")
        c.save("data-dump/final.csv")
        c.tweet_graph("I've been at @UCL's #ItsAllAcademic festival today learning to play Noughts & Crosses. This graph shows my learning progress. Thanks for teaching me!")
    else:
        c.save("data-dump/resume.json")
        c.save("data-dump/resume.csv")
except:
    pass
c.end()
