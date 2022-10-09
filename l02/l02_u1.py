slovo = list(input('Zadejte slovo: '))
slovo1 = [''] * len(slovo)
pocet = len(slovo)
pocet -= 1

for x in slovo:
    slovo1[pocet] = x
    pocet -= 1

print(''.join(slovo1))
