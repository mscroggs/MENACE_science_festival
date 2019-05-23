#!/usr/bin/env python
import data_collector
import sys

c = data_collector.Collector()

c.TWEETING = False

if len(sys.argv)>1 and sys.argv[1] == "tweet":
    c.Tweeting = True

c.filename = "data-dump/final-sim.json"

try:
    c.simulate()
except KeyboardInterrupt:
    c.save("data-dump/final-sim.json")
    c.save("data-dump/final-sim.csv")
