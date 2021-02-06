import json

fname = 'C:/Users/Jonathan Guo/Desktop/pokesearch/pokelist.txt'
f = open(fname, 'r')

pokes = []
for line in f:
    pokes.append(json.loads(line))

results = []
for poke in pokes:
    defog = ''
    spin = ''
    types = []

    moves = poke['moves']
    for move in moves:
        name = move['move']['name']
        if str(name) == 'defog':
            defog = 'defog'
        elif str(name) == 'rapid-spin':
            spin = 'rapid-spin'
    
    for t in poke['types']:
        types.append(t['type']['name'])

    if 'ghost' in types and (defog != '' or spin != ''):
        print(poke['name'], defog, spin)

