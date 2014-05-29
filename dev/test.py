#!/usr/bin/env python3

import sys
import os.path
dev_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, dev_path)

import inotify.log
import inotify.adapters

#with inotify.adapters.Inotify() as i:
#    print("Here.")
