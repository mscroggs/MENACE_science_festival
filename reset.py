#!/usr/bin/env python
import data_collector
import sys

c = data_collector.Collector()
#c.plot_etc()

import os

if not os.path.isdir("data-dump"):
    os.system("mkdir data-dump")
os.system("rm data-dump/*")
