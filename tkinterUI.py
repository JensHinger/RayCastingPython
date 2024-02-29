import tkinter as tk
from tkinter import ttk
from map import Map
from vector import Vector
import math

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Create Map
        self.map = Map()
        # TODO change to load map from some file? -> Json?´
        self.map.create_test_map()

        #
        # Start Game frame
        #
        self.game_frame = ttk.Frame(
            self,
            border=1,
        )
        self.game_frame.grid(
            column=1,
            row=1,
            sticky=tk.NSEW
        )

        self.game_canvas = tk.Canvas(
            self.game_frame,
            width=self.map.map_size,
            height=self.map.map_size,
            background="black",
        )
        self.game_canvas.pack()

        self.draw_map()        

        self.ray_amount = 360
        self.player_r = 5
        self.player_pos = Vector(int(self.map.map_size / 2), int(self.map.map_size / 2))
        self.ray_dir_vecs = []
        self.rays = []
        self.current_intersects = []

        self.init_ray_dir_vecs(self.ray_amount)
        self.player = self.draw_player(self.player_pos.x, self.player_pos.y)
        
        self.game_canvas.bind("<Motion>", self.move_player)

        self.mainloop()

    def draw_map(self):
        for wall in self.map.walls:
            self.game_canvas.create_line(wall[0].x, wall[0].y, wall[1].x, wall[1].y, fill="#ffffff")

    def init_ray_dir_vecs(self, amount_rays):
        for deg in range(0, 360, int(360/ amount_rays)):
            self.ray_dir_vecs.append(
                Vector(
                    math.cos(deg * (math.pi / 180)),
                    math.sin(deg * (math.pi / 180))
                )
            )

    def draw_player(self, x, y):
        # Always draw player at specified position
        player = self.game_canvas.create_oval(
            x-self.player_r, y-self.player_r,
            x+self.player_r, y+self.player_r,
            fill="white", 
            width=0)
        return player
    
    def calc_wall_intersect(self):
        x1, y1 = self.player_pos
        
        for ray in self.ray_dir_vecs:
            x2, y2 = ray + self.player_pos 
            closest_intersect = math.inf

            for wall in self.map.walls:
                x3, y3 = wall[0]
                x4, y4 = wall[1]

                det = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

                if det == 0:
                    continue
                
                t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / det
                u = - (((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / det)

                if 0 <= u <= 1 and t >= 0:
                    if t < closest_intersect:
                        closest_intersect = t

            ray_length = max(closest_intersect, 0)
            intersect_vec = self.player_pos + (ray * ray_length)
            self.create_intersect_circle(intersect_vec, 2)
            self.create_intersect_ray(self.player_pos, intersect_vec)

    def create_intersect_circle(self, vec, size):
        self.current_intersects.append(
                self.game_canvas.create_oval(
                    vec.x - size,
                    vec.y - size,
                    vec.x + size,
                    vec.y + size,
                    fill="red"
                )
            )

    def create_intersect_ray(self, vec_a, vec_b):
        self.rays.append(
                self.game_canvas.create_line(
                    vec_a.x, vec_a.y,
                    vec_b.x, vec_b.y,
                    fill="#ffffff"
                )
            )

    #
    # Events
    #

    def move_player(self, event):
        for intersect in self.current_intersects:
            self.game_canvas.delete(intersect)
        self.current_intersects = []

        for ray in self.rays:
            self.game_canvas.delete(ray)
        self.rays = []

        self.configure(cursor="none")
        self.game_canvas.delete(self.player)
        self.calc_wall_intersect()
        self.player_pos = Vector(event.x, event.y)
        self.player = self.draw_player(event.x, event.y)
        
if __name__ == "__main__":
    window = MainWindow()
    