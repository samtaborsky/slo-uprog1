def vytvor(n, x):
    m = [[x for a in range(n)] for b in range(n)]
    return m


def tisk(A):
    for x in A:
        for y in x:
            print('{0:5} '.format(y), end='')
        print()


def soucin(A, B):
    global C
    sloupce_a = len(A[0])
    sloupce_b = len(B[0])
    radky_a = len(A)
    radky_b = len(B)
    if sloupce_a != radky_b:
        exit('Spatne matice.')
    else:
        C = [[0 for x in range(sloupce_b)] for y in range(radky_a)]
        for r in range(radky_a):
            for s in range(sloupce_b):
                for i in range(radky_b):
                    C[r][s] += A[r][i] * B[i][s]
        return C


def nastav_okoli(A, i, j, c):
    """Funkce bere bezne indexy matic od 1 po N"""
    n = len(A) - 1
    i -= 1
    j -= 1
    if j < 0 or i < 0 or i > n or j > n:
        exit('Spatne zadane indexy!')
    A[i][j] = c
    if i == n:
        if j == 0:
            A[i][j+1] = c
            A[i-1][j] = c
        elif j == n:
            A[i][j-1] = c
            A[i-1][j] = c
        else:
            A[i][j-1] = c
            A[i][j+1] = c
            A[i-1][j] = c

    elif i == 0:
        if j == 0:
            A[i][j+1] = c
            A[i+1][j] = c
        elif j == n:
            A[i][j-1] = c
            A[i+1][j] = c
        else:
            A[i][j-1] = c
            A[i][j+1] = c
            A[i+1][j] = c

    else:
        if j == 0:
            A[i][j+1] = c
            A[i-1][j] = c
            A[i+1][j] = c
        elif j == n:
            A[i][j-1] = c
            A[i-1][j] = c
            A[i+1][j] = c
        else:
            A[i][j-1] = c
            A[i][j+1] = c
            A[i-1][j] = c
            A[i+1][j] = c
    return A


A = vytvor(5, 0)
nastav_okoli(A, 3, 3, 1)
tisk(A)
