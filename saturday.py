#!/usr/bin/env python
import data_collector
import sys

if "resume" in sys.argv:
    c = data_collector.Collector("data-dump/sat-resume.json")
else:
    c = data_collector.Collector()

if "test" in sys.argv:
    c.TWEETING = False

try:
    c.start()
except KeyboardInterrupt:
    print("Is is the end of the day? y/n ")
    end = c.prompt(["y","n"])
    if end=="y":
        c.save("data-dump/sat-final.json")
        c.save("data-dump/sat-final.csv")
        c.tweet_graph("I'm at @McrSciFest learning to play Noughts & Crosses. This graph shows my learning progress after day one. #msf17")
    else:
        c.save("data-dump/sat-resume.json")
        c.save("data-dump/sat-resume.csv")
except:
    pass
c.end()
