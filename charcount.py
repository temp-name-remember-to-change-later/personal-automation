#!/usr/bin/env python3
import sys

# This script takes in a file and prints out all the characters in that file along with the number of occurrences.
# Numbers and letters are included in the list by default, so if they don't occur, the number of occurrences will be reported as 0.

f = open(sys.argv[1], 'r')
ch = {}
nums = '0123456789'
letts = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSWXYZ'

for num in nums:
    ch[num] = 0
for lett in letts:
    ch[lett] = 0

for line in f:
    for char in line:
        if char in ch:
            ch[char] += 1
        else:
            ch[char] = 1

srt = []
for x in ch:
    srt.append((x, ch[x]))

for x in reversed(sorted(srt, key=lambda k: k[1])):
    if x[0] == '\n':
        print('\\n', x[1], sep=': ')
    else:
        print(x[0], x[1], sep=' : ')
