def nacti_bludiste(jmenosouboru):
    f = open(jmenosouboru, 'r')
    blud = []
    for s in f:
        s = s.strip('\n')
        blud.append(list(s))
    f.close()
    return blud


def opis_bludiste(blud):
    for radek in blud:
        for pole in radek:
            print(pole, end='')
        print()
    return


def rozlej(x, y, blud):
    if x < 0 or x >= len(blud) or y < 0 or y >= len(blud[0]) or blud[x][y] != ' ' or blud[x][y] == '@':
        return

    blud[x][y] = '@'
    rozlej(x - 1, y, blud)
    rozlej(x + 1, y, blud)
    rozlej(x, y - 1, blud)
    rozlej(x, y + 1, blud)


bludiste = nacti_bludiste('bludiste.txt')

opis_bludiste(bludiste)
print()
rozlej(1, 7, bludiste)
opis_bludiste(bludiste)
