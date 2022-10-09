import random

podmet = ['Otec', 'Auto', 'Stát', 'Krajina']
prisudok = ['jede', 'stojí', 'mluví', 'přemýšlí']
privlastok = ['velké', 'rychlé', 'inteligentní', 'počítačové']
predmet = ['člověka', 'nebe', 'hory', 'restauraci']
prislovkove_urcenie = ['včera', 'pryč', 'mezitím', 'vesele']

for i in range(4):
    a = random.choice(podmet)
    b = random.choice(prisudok)
    c = random.choice(privlastok)
    d = random.choice(predmet)
    e = random.choice(prislovkove_urcenie)
    print(f'{a} {e} {b} {c} {d}')
