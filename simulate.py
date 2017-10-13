#!/usr/bin/env python
import data_collector

c = data_collector.Collector()

c.filename = "data-dump/final-sim.json"

try:
    c.simulate()
except KeyboardInterrupt:
    c.save("data-dump/final-sim.json")
    c.save("data-dump/final-sim.csv")
