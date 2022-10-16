veta = str(input('Zadejte vetu: '))
if veta[-1] == '.':
    veta = veta[:-1]
veta = veta[0].lower() + veta[1:]
veta = veta.split()
n = len(veta) - 1
veta_new = ''

for _ in range(len(veta)):
    if n == 0:
        veta_new += veta[n]
    else:
        veta_new += veta[n] + ' '
    n -= 1

veta_new = veta_new[0].upper() + veta_new[1:]
veta_new += '.'

print(veta_new)
