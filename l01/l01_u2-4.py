import numpy as np

koeficienty = []

print('Rovnica a*x^3 + b*x^2 + c*x + d = 0')

try:
    koeficienty.append(float(input('a = ')))
    koeficienty.append(float(input('b = ')))
    koeficienty.append(float(input('c = ')))
    koeficienty.append(float(input('d = ')))
except ValueError:
    print('Koeficienty musia byt realne cisla')
else:
    riesenia = np.roots(koeficienty)
    print(riesenia)
