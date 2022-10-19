import random

souhlasky = ['h', 'ch', 'k', 'r', 'd', 't', 'n', 'b', 'f', 'l', 'm', 'p', 's', 'v', 'z', 'c', 'j']
samohlasky = ['a', 'e', 'i', 'o', 'u']
slova = []
slovo = ''

for y in range(1, random.randint(1, 10)):
    for x in range(3, random.randint(3, 10)):
        slovo += random.choice(souhlasky)
        slovo += random.choice(samohlasky)
    slova.append(slovo)
    slovo = ''

n = 0
for x in slova:
    print(f'{n} {x}')
    n += 1
