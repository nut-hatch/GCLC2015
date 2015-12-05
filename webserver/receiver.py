#!/usr/bin/env python

import socket
import re
import zlib
import collections
    
#TCP receiving socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('51.255.62.63', 10005))
s.listen(1)

cache = collections.OrderedDict()
counter = 0

while 1:
    conn, addr = s.accept()
    while 1:
        data = conn.recv(4096)
        #Decompress
        try: 
            data = zlib.decompress(data)
        except:
            print("Wrong d " + data)
            
        if re.match("^([#][0-9]+\s.*)$", data): #Get from cache
            refdata = data.split(" ", 1)
            data = refdata[1]+" "+cache[int(refdata[0][1:])]
        elif len(data) >= 130: #Store to cache treshold
            if len(cache) > 101:
                cache.popitem(False)
            splitdata = data.split(" ", 4)
            cache[counter] = splitdata[4]
        counter += 1

        #Log
        with open("/opt/gclc/gclc.log", "a") as myfile:
            myfile.write(data)
            myfile.close()

conn.close()