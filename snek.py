#!/usr/bin/env python3
import random

# unfinished beginnings of a CLI snake game

# characters used to make the snek
v = '│'
h = '─'
tl = '┌'
tr = '┐'
bl = '└'
br = '┘'
head = '☻'

# characters used to denote directions
u = 'u'
d = 'd'
l = 'l'
r = 'r'

# prints grid
def printgrid(mat):
    for row in mat:
        for ch in row:
            print(ch, end='')
        print()

# grid parameters
hlength = 60
vlength = 15

# constructs grid
top = [h for _ in range(hlength)]
top[0] = tl
top[hlength - 1] = tr

bot = [h for _ in range(hlength)]
bot[0] = bl
bot[hlength - 1] = br

mid = [' ' for _ in range(hlength)]
mid[0] = v
mid[hlength - 1] = v

grid = [[x for x in mid] for _ in range(vlength)]
grid.insert(0, top)
grid.append(bot)

init_dir = random.choice([u, l, d, r])
game_over = False
while(not game_over):
    print(init_dir)