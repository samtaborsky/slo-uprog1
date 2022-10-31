from time import *

cisla = []
time2 = time() + 10

while time() < time2:
    try:
        n = float(input('Zadejte cele cislo: '))
        if n in cisla:
            raise TypeError
        else:
            cisla.append(n)
    except ValueError:
        print('Spatny input.')
    except TypeError:
        print('Duplicitny vstup')

print()
print(cisla)
