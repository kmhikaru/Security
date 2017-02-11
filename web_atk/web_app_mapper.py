# -*- coding: utf-8 -*-

import Queue
import threading
import os
import urllib2

threads = 10

target = "http://www.blackhatpython.com"
directory = "/"
