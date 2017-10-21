#!/usr/bin/env python
import data_collector
import sys
from time import sleep

if "resume" in sys.argv:
    c = data_collector.Collector("data-dump/sun-resume.json")
else:
    c = data_collector.Collector("data-dump/sat-final.json")

if "test" in sys.argv:
    c.TWEETING = False

try:
    c.start()
except KeyboardInterrupt:
    print("Is is the end of the day? y/n ")
    end = c.prompt(["y","n"])
    while end not in ["y","n"]:
        end = input("What?! Is is the end of the day? y/n ").lower()
    if end=="y":
        c.save("data-dump/sun-final.json")
        c.save("data-dump/sun-final.csv")
        c.tweet_graph("I've been at @McrSciFest learning to play Noughts & Crosses. This graph shows my learning progress after day two. #msf17")
        sleep(2)
        c.tweet("Bye bye @McrSciFest, I've had lots of fun games of Noughts & Crosses! #msf17")
    else:
        c.save("data-dump/sun-resume.json")
        c.save("data-dump/sun-resume.csv")
except:
    pass

c.end()
