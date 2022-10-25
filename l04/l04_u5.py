def key_pocet(w):
    return w[1]


frekv = {}

with open('text.txt', 'r', encoding='utf-8') as f:
    for line in f:
        for word in line.split():
            if word in frekv:
                frekv[word] += 1
            else:
                frekv[word] = 1

    sorted_frekv = sorted(frekv.items(), key=key_pocet, reverse=True)

print('10 nejcastejsich slov')
for x in range(10):
    print(f'{x+1}. {sorted_frekv[x][0]} - {sorted_frekv[x][1]}x')
