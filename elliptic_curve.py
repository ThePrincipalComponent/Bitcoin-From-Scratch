from modular_inverse import inv

class Curve:
    # y^2 = x^3 + ax +b
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

class Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def is_on_curve(self):
        lhs = (self.y**2) % self.curve.p
        rhs = (self.x**3 + self.curve.a*self.x + self.curve.b) % self.curve.p
        return round(lhs, 6) == round(rhs, 6)

    def __add__(self, other):
        if not (self.is_on_curve() and other.is_on_curve()):
            raise TypeError('Points are not on curve.')
        
        if not (isinstance(self, Point) and isinstance(other, Point)):
            raise TypeError('Expected objects of class Point.')

        if self.x==None:
            return other
        
        if other.x==None:
            return self

        # points are inverses of each other
        if self.x == other.x and self.y == -(other.y-self.curve.p):
            return Point(x=None, y=None, curve=self.curve)

        # points are different
        if self.x != other.x:
            m = (other.y - self.y) * inv(other.x - self.x, self.curve.p)

        # points are the same, aka point doubling
        if self.x == other.x and self.y == other.y:
            m = (3*self.x**2 + self.curve.a) * inv(2*self.y, self.curve.p)
        
        x3 = (m**2 - self.x - other.x) % self.curve.p
        y3 = (-(m * (x3 - self.x) + self.y)) % self.curve.p
        
        return Point(x=x3, y=y3, curve=self.curve)
    
    def __mul__(self, other):
        track = [(1, self)]
        while (track[-1][0] + track[-1][0]) < other:
            track.append( (track[-1][0] + track[-1][0], track[-1][1] + track[-1][1]) )

        for tracker, result in reversed(track):
            if (track[-1][0] + tracker) <= other:
                track.append( (track[-1][0] + tracker, track[-1][1] + result))
        
        return track[-1][1]

bitcoin_curve = Curve(
    a = 0,
    b = 7,
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)

bitcoin_G = Point(
    x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
    curve = bitcoin_curve
)

if __name__ == '__main__':
    print(bitcoin_G.is_on_curve())
    g3 = bitcoin_G*3
    print(g3.is_on_curve())