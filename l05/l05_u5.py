import time


class Bod:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def zobraz(self):
        print("Bod:  x = ", self.x, " y = ", self.y)

    def translace(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return "({0.x:.3f}, {0.y:.3f})".format(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Bod2G(Bod):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y)
        self.vx = float(vx)
        self.vy = float(vy)

    def __str__(self):
        return super().__str__()+" [{0.vx:.3f}, {0.vy:.3f}]".format(self)

    def __eq__(self, other):
        return self.vx == other.vx and self.vy == other.vy and super().__eq__(other)

    def krok(self):
        self.translace(self.vx, self.vy)
        self.vy -= 10


b = Bod2G(0.0, 100.0, 3.0, 100.0)
t = 0
print("t[s] x[m]  y[m]  vx[m/s]  vy[m/s]")
print(t, b)

while True:
    b.krok()
    t += 1
    print(t, b)
    time.sleep(1)
