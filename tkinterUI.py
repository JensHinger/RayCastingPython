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

        self.player_r = 5
        self.player_pos = Vector(int(self.map.map_size / 2), int(self.map.map_size / 2))
        self.ray_dir_vecs = []
        self.rays = []
        self.current_intersects = []

        self.init_ray_dir_vecs(6)
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
        q = self.player_pos

        for s in self.ray_dir_vecs:
            for w in self.map.walls:
                p = w.loc_vec
                r = w.dir_vec

                rxs = r * s
                p_q = (q - p)

                p_qxs = p_q * s

                if rxs == 0 and p_qxs != 0:
                    continue
                elif rxs != 0:
                    u = ((-p_q) * r) / (-rxs)
                    t = p_qxs / rxs

                    if 0 <= t <= 1:
                        # TODO Shoudl only show intersects closeset to the player

                        intersect_vec = q + (s * u)

                        self.current_intersects.append(
                            self.game_canvas.create_oval(
                                intersect_vec.x - 2,
                                intersect_vec.y - 2,
                                intersect_vec.x + 2,
                                intersect_vec.y + 2,
                                fill="red"
                            )
                        )

                        self.rays.append(
                            self.game_canvas.create_line(
                                self.player_pos.x, self.player_pos.y,
                                intersect_vec.x, intersect_vec.y,
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
    