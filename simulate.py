#!/usr/bin/env python
import data_collector
import sys

c = data_collector.Collector()

if len(sys.argv)>1 and sys.argv[1] == "test":
    c.TWEETING = False

c.filename = "data-dump/final-sim.json"

try:
    c.simulate()
except KeyboardInterrupt:
    c.save("data-dump/final-sim.json")
    c.save("data-dump/final-sim.csv")
