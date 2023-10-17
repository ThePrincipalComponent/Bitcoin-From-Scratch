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
        lhs = self.y**2
        rhs = self.x**3 + self.curve.a*self.x + self.curve.b

        return round(lhs, 6) == round(rhs, 6)

    def __add__(self, other):
        if not (self.is_on_curve() and other.is_on_curve()):
            raise TypeError('Points are not on curve.')
        
        if not (isinstance(self, Point) and isinstance(other, Point)):
            raise TypeError('Expected objects of class Point.')

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

bitcoin_curve = Curve(
    a = 0,
    b = 7,
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)

if __name__ == '__main__':
    point1 = Point(x=1, y=8**(1/2), curve=bitcoin_curve)
    point2 = Point(x=2, y=15**(1/2), curve=bitcoin_curve)
    point3 = point1 + point2
    point4 = point1 + point1
    print(point3.x, point3.y)
    print(point4.x, point4.y)
    print('\n')

    print(f'point1 is on curve: {point1.is_on_curve()}')
    print(f'point3 is on curve: {point3.is_on_curve()}')