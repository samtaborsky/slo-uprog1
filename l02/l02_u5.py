import random

n = 5
print('01234567890')
mezera = ' '

while n < 10:
    if n == 0:
        n = random.randint(n, n+1)
    else:
        n = random.randint(n-1, n+1)
    print(mezera*(n-1) + '*')

print('01234567890')
print('ŽBLUŇK!')
