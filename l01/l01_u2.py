samohlasky = ['a', 'e', 'i', 'o', 'u']

a = list(input('Zadejte text: '))
i = 0

for x in a:
    if x in samohlasky:
        a[i] = 'a'
    i += 1

print(''.join(a))
