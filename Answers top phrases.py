#!/usr/bin/env python
# coding: utf-8

# In[ ]:


Lets say i have a text file of 1000 GB. I need to find how much times a phrase occurs in the text


# In[ ]:


phrase = "how fast it is"
count = 0
with open('bigfile.txt') as f:
    for line in f:
        count += line.count(phrase)


# In[ ]:


import os
import threading

INPUTFILE ='bigfile.txt'
SEARCH_STRING='how fast it is'
THREADS = 8  # Set to 2 times number of cores, assuming hyperthreading
CHUNK_SIZE = 32768

FILESIZE = os.path.getsize(INPUTFILE)
SLICE_SIZE = FILESIZE / THREADS



class myThread (threading.Thread):
    def __init__(self, filehandle, seekspot):
        threading.Thread.__init__(self)
        self.filehandle = filehandle
        self.seekspot = seekspot
        self.cnt = 0
    def run(self):
        self.filehandle.seek( self.seekspot )

        p = self.seekspot
        if FILESIZE - self.seekspot < 2 * SLICE_SIZE:
            readend = FILESIZE
        else: 
            readend = self.seekspot + SLICE_SIZE + len(SEARCH_STRING) - 1
        overlap = ''
        while p < readend:
            if readend - p < CHUNK_SIZE:
                buffer = overlap + self.filehandle.read(readend - p)
            else:
                buffer = overlap + self.filehandle.read(CHUNK_SIZE)
            if buffer:
                self.cnt += buffer.count(SEARCH_STRING)
            overlap = buffer[len(buffer)-len(SEARCH_STRING)+1:]
            p += CHUNK_SIZE

filehandles = []
threads = []
for fh_idx in range(0,THREADS):
    filehandles.append(open(INPUTFILE,'rb'))
    seekspot = fh_idx * SLICE_SIZE
    threads.append(myThread(filehandles[fh_idx],seekspot ) )
    threads[fh_idx].start()

totalcount = 0 
for fh_idx in range(0,THREADS):
    threads[fh_idx].join()
    totalcount += threads[fh_idx].cnt

print totalcount


# In[ ]:


import os
import re
import mmap

fileName = 'bigfile.txt'
phrase = re.compile("how fast it is")

with open(fileName, 'r') as fHandle:
    data = mmap.mmap(fHandle.fileno(), os.path.getsize(fileName), access=mmap.ACCESS_READ)
    matches = re.match(phrase, data)
    print('matches = {0}'.format(matches.group()))

