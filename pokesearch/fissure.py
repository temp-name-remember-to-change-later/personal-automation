import json

fname = 'C:/Users/Jonathan Guo/Desktop/pokesearch/pokelist.txt'
f = open(fname, 'r')

ohkos = ['fissure', 'sheer-cold', 'horn-drill', 'guillotine']
locks = ['lock-on', 'mind-reader']

pokes = []
for line in f:
    pokes.append(json.loads(line))

results = []
for poke in pokes:
    ohko = ''
    lock = ''
    cp = False
    ng = False

    moves = poke['moves']
    for move in moves:
        name = move['move']['name']
        if str(name) in ohkos:
            ohko = str(name)
        if str(name) in locks:
            lock = str(lock)
        if str(name) == 'copycat':
            cp = True
    
    for a in poke['abilities']:
        if a['ability']['name'] == 'no-guard':
            ng = True
    
    if ohko != '' and lock != '':
        print(poke['name'], ohko, lock)
    elif ohko != '' and ng == True:
        print(poke['name'], ohko, 'no-guard')
    elif cp == True and ng == True:
        print(poke['name'], 'copycat', 'no-guard')

            


# import requests
# import json


# num_pokes = 899

# pokemon = []
# for i in range(1, num_pokes):
#     print('Loading pokemon {} of {}...'.format(i, num_pokes))
#     pokemon.append(
#         json.loads(
#             requests.get('https://pokeapi.co/api/v2/pokemon/{}'.format(i)).text
#         )
#     )

# output = []
# for poke in pokemon:
#     ohko = False
#     for move in poke['moves']:
#         if move['move']['name'] in ohkos:
#             ohko = True
#     if not ohko:
#         output.append(poke['name'])

# for poke in output:
#     print(poke)
