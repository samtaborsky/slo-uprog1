import random

n = random.randint(1, 2)
cisla = []

for x in range(n):
    c = round(random.uniform(0, 100), 2)
    cisla.append(c)

cisla.sort()

if len(cisla) == 1:
    median = cisla[0]

elif len(cisla) == 2:
    print(cisla)
    median = round((cisla[0] + cisla[1]) / 2, 2)

else:
    pocet = len(cisla)
    opak = 1
    while pocet > 2:
        print(f'---{opak}---')
        print(f'Prvni cislo: {cisla[0]}')
        del cisla[0]
        print(f'Posledni cislo: {cisla[-1]}')
        del cisla[-1]
        pocet -= 2
        opak += 1
    print('-------')
    if pocet == 2:
        print(cisla)
        median = round((cisla[0] + cisla[1]) / 2, 2)
    else:
        median = cisla[0]

print(f'Median: {median}')
