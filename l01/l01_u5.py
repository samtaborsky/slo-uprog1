import random


def hod(pocet, strany):
    vysledok = []
    for x in range(pocet):
        vysledok.append(random.randint(1, strany))
    return vysledok


try:
    n = int(input('Pocet hodov N: '))
    m = int(input('Pocet stien kocky M: '))
except ValueError:
    print('N a M musia byt cele cisla')
else:
    print(f'Vysledne cisla: {hod(n, m)}')
