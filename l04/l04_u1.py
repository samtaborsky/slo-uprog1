souhlasky_list = ['h', 'H', 'ch', 'CH', 'k', 'K', 'r', 'R', 'd', 'D', 't', 'T', 'n', 'N', 'b', 'B', 'f', 'F',
                  'l', 'L', 'm', 'M', 'p', 'P', 's', 'S', 'v', 'V', 'z', 'Z', 'c', 'C', 'j', 'J', 'g', 'G',
                  'x', 'X', 'q', 'Q', 'w', 'W', 'y', 'Y']
samohlasky_list = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
frekv = {chr(x): 0 for x in range(ord('a'), ord('z')+1)}

with open('text.txt', mode='r', encoding='utf-8') as o, open('samohlasky-u1.txt', mode='w', encoding='utf-8') as \
        samohlasky, open('souhlasky-u1.txt', mode='w', encoding='utf-8') as souhlasky:

    while 1:
        znak = o.read(1)
        if znak != '':
            if ord('a') <= ord(znak) <= ord('z') or ord('A') <= ord(znak) <= ord('Z'):
                frekv[znak.lower()] += 1
        if znak in souhlasky_list:
            souhlasky.write(znak)
        elif znak in samohlasky_list:
            samohlasky.write(znak)
        else:
            souhlasky.write(znak)
            samohlasky.write(znak)
        if znak == '':
            break

print('Frekvence pismen (velkych i malych spolu)')
for x in frekv:
    if frekv[x] != 0:
        print(x, '->', frekv[x])
