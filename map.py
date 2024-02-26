from vector import Vector
from line import Line

class Map:

    def __init__(self) -> None:
        self.map_size = 0
        self.walls = []

    def load_map_file(self, file_location):
        pass

    def create_test_map(self):
        self.map_size = 1000

        #    middle walls hori    middle walls      triangles
        x = [400, 600, 400, 600, 250, 250, 750, 750, 200, 50, 50, 250, 250, 200, 200, 50, 50, 250, 250, 200]
        y = [600, 600, 400, 400, 200, 800, 200, 800, 800, 950, 950, 950, 950, 800, 200, 50, 50, 50, 50, 200]


        for i in range(0,len(x), 2):
            v_1 = Vector(x[i], y[i])
            v_2 = Vector(x[i+1], y[i+1])

            self.walls.append(Line(v_1, v_2))

if __name__ == "__main__":
    m = Map()
    m.create_test_map()