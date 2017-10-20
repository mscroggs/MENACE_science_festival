#!/usr/bin/env python
import data_collector

c = data_collector.Collector()

try:
    c.start()
except KeyboardInterrupt:
    c.save("data-dump/final.json")
    c.save("data-dump/final.csv")
except:
    pass

c.end()
