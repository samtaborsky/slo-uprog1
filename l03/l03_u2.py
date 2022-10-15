def vytvor_krychli(n, cislo):
    m = [[[cislo for _ in range(n)] for _ in range(n)] for _ in range(n)]
    return m


def opis_krychli(krychle):
    print('---')
    for i in krychle:
        for j in i:
            for k in j:
                print('{0:2} '.format(k), end='')
            print()
        print('---')


def nastav_uhlopricku(n, cislo):
    """Vyber tel. uhl. 1-4 a nastav ji na cislo X
    !! JEN PRO KRYCHLE 4x4x4 !!"""
    if n < 1 or n > 4:
        exit('Spatne N!')
    if n == 1:
        j = 0
        k = 0
        for i in range(4):
            A[i][j][k] = cislo
            i += 1
            j += 1
            k += 1

    elif n == 2:
        j = 0
        k = 3
        for i in range(4):
            A[i][j][k] = cislo
            i += 1
            j += 1
            k -= 1

    elif n == 3:
        j = 3
        k = 0
        for i in range(4):
            A[i][j][k] = cislo
            i += 1
            j -= 1
            k += 1

    elif n == 4:
        j = 3
        k = 3
        for i in range(4):
            A[i][j][k] = cislo
            i += 1
            j -= 1
            k -= 1

    else:
        exit('Spatne N!')


A = vytvor_krychli(4, 0)

for x in range(4):
    x += 1
    nastav_uhlopricku(x, x)

opis_krychli(A)
