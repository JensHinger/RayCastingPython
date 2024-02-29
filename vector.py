class Vector:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}"
    
    def __sub__(self, other):
        return self.__add__(-other)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        if type(other) is Vector:
            return self.x * other.y - other.x * self.y
        else:
            return Vector(self.x * other, self.y * other)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __iter__(self):
        return iter((self.x, self.y))