#!/usr/bin/env python3
import hashlib
import random
import string
import threading
import sys

# Basic multithreaded script
# Attempts to find random (alphanumeric) strings of the same length as the input string,
# whose hashes match that of the input string up to a certain number of places

# Takes in a string and a number
try:
    instr = sys.argv[1]
    places = int(sys.argv[2])
except:
    print('usage: sha.py <string> <number>')

def randomString(stringLength=len(instr)):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def findstuff():
    m = hashlib.sha256()
    m.update(instr.encode('utf-8'))
    tomatch = m.hexdigest()

    matches = []
    while(True):
        randomstr = randomString()
        n = hashlib.sha256(randomstr.encode('utf-8')).hexdigest()
        if n[0:places] == tomatch[0:places]:
            matches.append(randomString())
            print(randomstr, n, sep='; hash: ')

class thread(threading.Thread):
    def run(self):
        findstuff()

threads = []
for i in range(12):
    threads.append(thread())

for thr in threads:
    thr.start()
