import math


def eratosthenovo_sito(pocet):
    pocet += 1
    cisla = [True] * pocet
    prvocisla = []

    for x in range(2, pocet):
        if cisla[x] is True:
            for i in range(x**2, pocet, x):
                cisla[i] = False

    for x in range(2, pocet):
        if cisla[x] is True:
            prvocisla.append(x)

    return prvocisla


def rozklad_na_prvocisla(cislo):
    odmocnina = int(math.sqrt(cislo))
    prvocisla = eratosthenovo_sito(odmocnina)
    rozklad = []

    for a in prvocisla:
        while cislo % a == 0:
            rozklad.append(a)
            cislo /= a

    if cislo != 1:
        rozklad.append(int(cislo))

    return rozklad


try:
    n = int(input('Zadejte cislo: '))
except ValueError:
    print('Zadejte cele cislo.')
else:
    vysledok = rozklad_na_prvocisla(n)
    print(f'Rozklad cisla {n} na prvocisla je {vysledok}')
