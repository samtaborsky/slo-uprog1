import time
from l05.l05_u5 import Bod2G


class Bod2GG(Bod2G):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy)

    def __str__(self):
        return super().__str__()

    def __eq__(self, other):
        return super().__eq__(other)

    def krok(self):
        if abs(self.y) - abs(self.vy) <= 0:
            temp_y = -self.y
            temp_vy = self.vy
            self.vy = temp_y
            super().krok()
            self.vy = abs(temp_vy) - abs(temp_y)
            super().krok()
        else:
            super().krok()


b = Bod2GG(0.0, 100.0, 0.0, 50.0)
t = 0
print("t[s] x[m]  y[m]  vx[m/s]  vy[m/s]")
print(t, b)

while True:
    b.krok()
    t += 1
    print(t, b)
    time.sleep(1)
