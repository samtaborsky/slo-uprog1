from time import *
from random import *

t1 = localtime()
print(t1)
print('Od ', end='')
print(strftime('%d.%m.%y %H:%M', t1))
t2 = list(t1)
t2[0] += 1
t2[1] = 1
t2[2] = 1
for i in range(3, 6):
    t2[i] = 0

t2 = struct_time(t2)
print('Do ', end='')
print(strftime('%d.%m.%y %H:%M', t2))
print()

t1s = int(mktime(t1))
t2s = int(mktime(t2))

for x in range(10):
    tr = localtime(randint(t1s, t2s))
    tr_format = strftime('%d.%m.%y %H:%M', tr)
    print(tr_format)





