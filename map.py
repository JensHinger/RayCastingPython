from vector import Vector
from line import Line

class Map:

    def __init__(self) -> None:
        self.map_size = 0
        self.walls = []

    def load_map_file(self, file_location):
        pass

    def create_test_map(self):
        self.map_size = 650

        x = [60, 600, 600, 30]
        y = [60, 20, 600, 620]

        for i in range(len(x)):
            v_1 = Vector(x[i], y[i])
            v_2 = Vector(x[(i+1) % len(x)], y[(i+1 )% len(x)])

            self.walls.append(Line(v_1, v_2))

if __name__ == "__main__":
    m = Map()
    m.create_test_map()