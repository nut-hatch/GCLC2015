#!/usr/bin/env python

import socket
import datetime
import time
import zlib
import collections

# Receiver UDP socket
receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(("", 514))

# Sending TCP socket
sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 1)
sender.connect(('51.255.62.63', 10005))

msg = ""
cache = collections.OrderedDict()
counter = 0

while 1:
    data, addr = receiver.recvfrom(4096)
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%b  %-d %H:%M:%S')
    
    if len(data) > 120: #Treshold
        if data in cache.keys(): #Get from cache
            msg = "#" + str(cache[data]) + " " + date #Replace string with msg reference
        else: #Store in cache
            if len(cache) > 100: #cache limited to 100 string to overuse memory
                cache.popitem(False)
            cache[data] = counter #Save in cache
            msg = " ".join([date,data])
    else: #Ignore cache
        msg = " ".join([date,data])
    counter += 1
    
    msg = zlib.compress(msg) #Compress
    sender.send(msg) #Send
