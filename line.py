from vector import Vector

class Line:

    def __init__(self, v_a: Vector, v_b:Vector) -> None:
        self.line = (v_a, v_b)

    def __getitem__(self, index) -> Vector:
        return self.line[index]