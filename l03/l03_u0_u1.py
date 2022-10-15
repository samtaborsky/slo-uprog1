def vytvor(n, x):
    m = [[x for _ in range(n)] for _ in range(n)]
    return m


def tisk(matice):
    for x in matice:
        for y in x:
            print('{0:5} '.format(y), end='')
        print()


def soucin(matice_a, matice_b):
    sloupce_a = len(matice_a[0])
    sloupce_b = len(matice_b[0])
    radky_a = len(matice_a)
    radky_b = len(matice_b)
    if sloupce_a != radky_b:
        exit('Spatne matice.')
    else:
        matice_c = [[0 for _ in range(sloupce_b)] for _ in range(radky_a)]
        for r in range(radky_a):
            for s in range(sloupce_b):
                for i in range(radky_b):
                    matice_c[r][s] += matice_a[r][i] * matice_b[i][s]
        return matice_c


def nastav_okoli(matice_a, i, j, c):
    """Funkce bere bezne indexy matic od 1 po N"""
    n = len(matice_a) - 1
    i -= 1
    j -= 1
    if j < 0 or i < 0 or i > n or j > n:
        exit('Spatne zadane indexy!')
    matice_a[i][j] = c
    if i == n:
        if j == 0:
            matice_a[i][j+1] = c
            matice_a[i-1][j] = c
        elif j == n:
            matice_a[i][j-1] = c
            matice_a[i-1][j] = c
        else:
            matice_a[i][j-1] = c
            matice_a[i][j+1] = c
            matice_a[i-1][j] = c

    elif i == 0:
        if j == 0:
            matice_a[i][j+1] = c
            matice_a[i+1][j] = c
        elif j == n:
            matice_a[i][j-1] = c
            matice_a[i+1][j] = c
        else:
            matice_a[i][j-1] = c
            matice_a[i][j+1] = c
            matice_a[i+1][j] = c

    else:
        if j == 0:
            matice_a[i][j+1] = c
            matice_a[i-1][j] = c
            matice_a[i+1][j] = c
        elif j == n:
            matice_a[i][j-1] = c
            matice_a[i-1][j] = c
            matice_a[i+1][j] = c
        else:
            matice_a[i][j-1] = c
            matice_a[i][j+1] = c
            matice_a[i-1][j] = c
            matice_a[i+1][j] = c

    return matice_a


A = vytvor(5, 0)
nastav_okoli(A, 3, 3, 1)
tisk(A)
