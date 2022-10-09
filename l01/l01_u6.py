samohlasky = ['a', 'e', 'i', 'o', 'u']

a = list(input('Zadejte text: '))
i = 0
pos = []

for x in a:
    if x in samohlasky:
        pos += [i]
    i += 1

pos.reverse()

for m in pos:
    a.pop(m)

print(''.join(a))
