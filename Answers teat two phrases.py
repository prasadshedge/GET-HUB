#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##Given a large file that does not fit in memory (say 10GB), find the top 100000 most frequent phrases. The file has 50 phrases per line separated by a pipe (|). Assume that the phrases do not contain pipe.
  Example line may look like: Foobar Candy | Olympics 2012 | PGA | CNET | Microsoft Bing ….
  The above line has 5 phrases in visible region.


I have a text file of 1000 GB. I need to find how much times a phrase occurs in the text.

Is there any faster way to do this that the one i am using bellow? How much would it take to complete the task.

phrase = "how fast it is"
count = 0
with open('bigfile.txt') as f:
    for line in f:
        count += line.count(phrase)
If I am right if I do not have this file in the memory i would meed to wait till the PC loads the file each time I am doing the search and this should take at least 4000 sec for a 250 MB/sec hard drive and a file of 10000 GB.

Code:

 from functools import partial

 def read_in_chunks(size_in_bytes):

    s = 'Lets say i have a text file of 1000 GB'
    with open('data.txt', 'r+b') as f:
        prev = ''
        count = 0
        f_read  = partial(f.read, size_in_bytes)
        for text in iter(f_read, ''):
            if not text.endswith('\n'):
                # if file contains a partial line at the end, then don't
                # use it when counting the substring count. 
                text, rest = text.rsplit('\n', 1)
                # pre-pend the previous partial line if any.
                text =  prev + text
                prev = rest
            else:
                # if the text ends with a '\n' then simple pre-pend the
                # previous partial line. 
                text =  prev + text
                prev = ''
            count += text.count(s)
        count += prev.count(s)
        print count
Timings:

read_in_chunks(104857600)
$ time python so.py
10000000

real    0m1.649s
user    0m0.977s
sys     0m0.669s

read_in_chunks(524288000)
$ time python so.py
10000000

real    0m1.558s
user    0m0.893s
sys     0m0.646s

read_in_chunks(1073741824)
$ time python so.py
10000000

real    0m1.242s
user    0m0.689s
sys     0m0.549s


read_in_chunks(2147483648)
$ time python so.py
10000000

real    0m0.844s
user    0m0.415s
sys     0m0.408s



On the other hand the simple loop version takes around 6 seconds on my system:

def simple_loop():

    s = 'Lets say i have a text file of 1000 GB'
    with open('data.txt') as f:
        print sum(line.count(s) for line in f)

$ time python so.py
10000000

real    0m5.993s
user    0m5.679s
sys     0m0.313s
Results of @SlaterTyranus's grep version on my file:

$ time grep -o 'Lets say i have a text file of 1000 GB' data.txt|wc -l
10000000

real    0m11.975s
user    0m11.779s
sys     0m0.568s

$ time cat data.txt | parallel --block 10M --pipe grep -o 'Lets\ say\ i\ have\ a\ text\ file\ of\ 1000\ GB' | wc -l
10000000

real    0m5.955s
user    0m14.825s
sys     0m5.766s
Got best timing when I used 100 MB as block size:

$ time cat data.txt | parallel --block 100M --pipe grep -o 'Lets\ say\ i\ have\ a\ text\ file\ of\ 1000\ GB' | wc -l
10000000

real    0m4.632s
user    0m13.466s
sys     0m3.290s
Results of woot's second solution:

$ time python woot_thread.py # CHUNK_SIZE = 1073741824
10000000

real    0m1.006s
user    0m0.509s
sys     0m2.171s
$ time python woot_thread.py  #CHUNK_SIZE = 2147483648
10000000

real    0m1.009s
user    0m0.495s
sys     0m2.144s



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

he way search engine works is by creating a mapping from words to the location they are in the file. Say if you have this file:
Foo bar baz dar. Dar bar haa.

create an index that looks like this:
{
    "foo": {0},
    "bar": {4, 21},
    "baz": {8},
    "dar": {12, 17},
    "haa": {25},
}

A hashtable index can be looked up in O(1); so it's freaking fast.

Final modified code :

import os
import re
import mmap

fileName = 'bigfile.txt'
phrase = re.compile("how fast it is")

with open(fileName, 'r') as fHandle:
    data = mmap.mmap(fHandle.fileno(), os.path.getsize(fileName), access=mmap.ACCESS_READ)
    matches = re.match(phrase, data)
    print('matches = {0}'.format(matches.group()))


