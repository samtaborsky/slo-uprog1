slovo = list(input('Zadejte slovo: '))
pocet = len(slovo)
slovo1 = [''] * pocet
pocet -= 1

for x in slovo:
    slovo1[pocet] = x
    pocet -= 1

print(''.join(slovo1))
