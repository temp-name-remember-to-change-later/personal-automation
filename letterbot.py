#!/usr/bin/env python3
import random
import os
import sys
import getopt

def consecutive(n, text):
    arr = []
    for i in range(len(text) - n):
        arr.append((text[i:i+n], text[i + n]))
    return arr

def gendic(textarr, depth):
    dic = {}
    text = '\n'.join(textarr)
    keys = consecutive(depth, text)
    for key in keys:
        if key[0] not in dic:
            dic[key[0]] = [key[1]]
        else:
            dic[key[0]].append(key[1])
    return dic

def parsetext(fname):
    textarr = []
    f = open(fname)
    for line in f:
        textarr.append(line)
    return textarr

def stdin():
    textarr = []
    for line in sys.stdin:
        textarr.append(line)
    return textarr


def gentext(seed, depth, length, dic):
    keys = list(dic.keys())
    if seed == '':
        seed = random.choice(keys)
    elif len(seed) < depth or seed[len(seed) - depth:] not in keys:
        seed = random.choice(keys)
    s = seed
    for i in range(length):
        s += random.choice(dic[s[len(s) - depth : len(s)]])
    return s

def main(argv):
    fname = ''
    depth = 0
    length = 0
    seed = ''

    try:
        opts, args = getopt.getopt(argv, "hf:d:l:s:")
    except getopt.GetoptError:
        print('usage: letterbot.py -f <filename> -d <depth> -l <length> -s <seed>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: letterbot.py -f <filename> -d <depth> -l <length> -s <seed>')
            sys.exit()
        elif opt == '-f':
            fname = arg
        elif opt == '-d':
            depth = int(arg)
        elif opt == '-l':
            length = int(arg)
        elif opt == '-s':
            seed = arg

    if depth == 0 or length == 0:
        print('usage: letterbot.py -f [filename] -d <depth> -l <length> -s [seed]')
        sys.exit(2)

    if fname == '':
        textarr = stdin()
    else:
        textarr = parsetext(fname)

    dic = gendic(textarr, depth)
    print(gentext(seed, depth, length, dic))

if __name__ == '__main__':
    main(sys.argv[1:])

