import requests

num_pokes = 1118

filename = 'C:/Users/Jonathan Guo/Desktop/pokelist.txt'
file = open('pokelist.txt', 'w')

for i in range(1, num_pokes + 1):
    print('Loading Pokemon {} of {}...'.format(i, num_pokes))
    file.write(requests.get('https://pokeapi.co/api/v2/pokemon/{}'.format(i)).text)
    file.write('\n')

print('Done')

file.close()