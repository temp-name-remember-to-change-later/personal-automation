#!/usr/bin/env python3
import sys
import subprocess
import re

# This simple script takes in a list of usernames from stdin.
# It then prints out the number of times each user has said the string given in the argument.
# (non-case-sensitive)

s = sys.argv[1]
for line in sys.stdin:
    outbytes = subprocess.run(['userdump.py', line], capture_output=True).stdout
    outstr = outbytes.decode('utf-8')
    print(line[:len(line) - 1], len(re.findall(s, outstr)), sep=': ')
