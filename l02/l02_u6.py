while True:
    try:
        n = int(input('Zadejte N: '))
        break
    except ValueError:
        print('Zadejte cele cislo N!')

text = '{0:<5d} {1:^10d} {2:^20.20f}'
i = 1

for x in range(1, n+1):
    power1 = 2**i
    power2 = (1/2)**i
    print(text.format(i, power1, power2))
    i += 1
