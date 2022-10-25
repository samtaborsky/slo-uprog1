import random

sifruj = {}
desifruj = {}
abeceda = 'abcdefghijklmnopqrstuvwxyz'


def generuj():
    for x in abeceda:
        y = random.choice(abeceda)
        while y in desifruj:
            y = random.choice(abeceda)
        else:
            sifruj[x] = y
            desifruj[y] = x


def subsif(x, slovnik):
    y = ""
    for z in x:
        if 'A' <= z <= 'Z':
            z = z.lower()
            z = slovnik[z]
            z = z.upper()
        elif 'a' <= z <= 'z':
            z = slovnik[z]
        else:
            z = z
        y += z
    return y


generuj()
print("Sifracni slovnik:", sifruj)
print("Inverzni desifracni slovnik:", desifruj)

s1 = str(input('Zadej text na zasifrovani: '))
s2 = subsif(s1, sifruj)
s3 = subsif(s2, desifruj)
print(s1, "->", s2, "->", s3)
