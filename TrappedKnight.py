#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:56:19 2019

@author: sgurvets
"""

import matplotlib.pyplot as plt

import numpy as np
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

import sys

#TODO classify object by standard deviation in x and y
#TODO create custom colormap cyclic (dark beginning and end?)

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


class Master:
    #sets up the simulation and builds file names
    def __init__(self, startx=1, starty=11,endx=41,endy=61):
        curx = startx
        while curx != endx:
            
            cury = starty
            while cury != curx:
                print("cur coords = "+str(curx)+"_"+str(cury))
                k = Knight(curx,cury,cmap="twilight",show="False",
                       filename="/Users/sgurvets/Documents/trappedknightpics_hightres_surveyto50/"+str(curx)+"_"+str(cury)+".png"
                       )
                del k
                cury=cury+1
                
            curx=curx+1

class Knight:
    #jumps around until trapped
    def __init__(self, dx=1, dy = 2, cmap='twilight', show="true",filename="defFig.png"):
        self.xstep = dx
        self.ystep = dy
        self.step_max = max(dx,dy)
        self.xstart = 0
        self.ystart = 0
        self.xpos = 0
        self.ypos = 0
        self.max_visited = 0
        self.x_visited = []
        self.y_visited = []
        self.n_visited = set()
        self.n_visited.add(1)
        self.grid = Grid()
        self.cmap = cmap
        self.filename = filename
        self.show = show
        for j in range(self.step_max):
                    self.grid.add_ring()
                    
        self.run()
                    
    def get_holes(self):
        all_n = set(i for i in range(1,self.max_visited+1))
        holes = all_n.difference(self.n_visited)
        return holes
    
    def update_max_visited(self, val):
        if val > self.max_visited:
            self.max_visited = val
        
    def run(self):
        step = True
        while step == True:
            step = self.step()
        print("squares visited = "+str(len(self.n_visited)))
        self.plot(self.cmap)
#        plt.plot(self.x_visited, self.y_visited, c=cm.hot() )
        
    def plot(self, cmap='viridis'):
        
        x = np.array(self.x_visited)
        y = np.array(self.y_visited)
        z = np.array([i for i in self.n_visited])
        
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        norm = plt.Normalize(z.min(), z.max())
        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(z)
        fig, axs = plt.subplots()
        
        line = axs.add_collection(lc)
        fig.colorbar(line)
        axs.set_xlim(x.min(), x.max())
        axs.set_ylim(y.min(), y.max())
#        axs.plot(x, y)
#        if self.show == True:
#            plt.show()
#        if self.show == False:
        plt.savefig(self.filename, dpi = 300)
        plt.close()
        print("saved")
        print(self.filename)
        
        
        
    def update_position(self, candidate):
        self.xpos = candidate[0]
        self.ypos = candidate[1]
        
        self.x_visited.append(candidate[0])
        self.y_visited.append(candidate[1])
        self.n_visited.add(candidate[2])
        
        
    def step(self):
        candidate = self.get_candidate()
        if candidate == "end":
            print("end")
            return False
        if candidate != "end":
            self.update_position(candidate)
            self.grid.update_grid_dict(candidate)
            self.update_max_visited(candidate[2])
            return True
            
        
    def get_candidate(self):
        x=self.xpos
        y=self.ypos
        dx=self.xstep
        dy=self.ystep
        cand_tuples = [(x+dx,y+dy),
                       (x-dx,y+dy),
                       (x+dx,y-dy),
                       (x-dx,y-dy),
                       (x+dy,y+dx),
                       (x-dy,y+dx),
                       (x+dy,y-dx),
                       (x-dy,y-dx)]
        candidate=(0,0,0)
        cur_min = float("inf")
        for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
            try:
                numfalse = self.grid.grid_dict[i]
            except KeyError:
                for j in range(self.step_max):
                    self.grid.add_ring()
                numfalse = self.grid.grid_dict[i]
                
            if numfalse[1]==False:
                if numfalse[0] < cur_min:
                    candidate = ((i[0],i[1],numfalse[0]))
                    cur_min = numfalse[0]
        #path is at an end
        if candidate == (0,0,0):
            return "end"
        return candidate
    
class HexGrid:
    def __init__(self):
        self.last_num = 1
        self.last_x = 0
        self.last_y = 0
        self.last_z = 0
        self.grid_dict = {}
        self.cur_ring = 1
        self.add_hex(x=0,y=0,z=0,num=1)
        #seeding the grid
        self.update_grid_dict((0,0,0,1))
        self.add_ring()
        
    def update_grid_dict(self, candidate):
        self.grid_dict[(candidate[0],candidate[1],candidate[2])]=(candidate[3],True)
        
    def add_ring(self):
        #add 1 down
        self.add_square(self.last_x, self.last_y-1,self.last_z+1,self.last_num+1)
        
        for i in range(self.cur_ring -1):
            self.add_hex(self.last_x-1,self.last_y,self.last_z+1,self.last_num+1)
        #add n left
        for i in range(self.cur_ring):
            self.add_square(self.last_x-1,self.last_y,self.last_num+1)
        #add n+1 up
        for i in range(self.cur_ring+1):
            self.add_square(self.last_x,self.last_y+1,self.last_z,self.last_num+1)
        #add n+1 right
        for i in range(self.cur_ring+1):
            self.add_square(self.last_x+1,self.last_y,self.last_num+1)
        #add n+1 down
        for i in range(self.cur_ring+1):
            self.add_square(self.last_x,self.last_y-1,self.last_num+1)
           #increases by 2 because we're adding 2 squares in each direction 
        self.cur_ring = self.cur_ring + 2
        
    def add_hex(self, x=0,y=0,z=0,num=1):
        self.grid_dict[(x,y,z)] = (num,False)
        self.last_x = x
        self.last_y = y
        self.last_z = z
        self.last_num = num
        
        
        
class Grid:
    def __init__(self):
        self.last_num = 1
        self.last_x = 0
        self.last_y = 0
        self.grid_dict = {}
        self.cur_ring=1
        self.add_square(x=0,y=0,num=1)
        #seeding the grid
        self.update_grid_dict((0,0,1))
        self.add_ring()
#        self.cur_ring = 3
        
    def update_grid_dict(self, candidate):
        #candidate is a tuple (x,y,num)
        self.grid_dict[(candidate[0],candidate[1])]=(candidate[2],True)
        
    def add_ring(self):
        #add 1 down
        self.add_square(self.last_x, self.last_y-1,self.last_num+1)
        #add n left
        for i in range(self.cur_ring):
            self.add_square(self.last_x-1,self.last_y,self.last_num+1)
        #add n+1 up
        for i in range(self.cur_ring+1):
            self.add_square(self.last_x,self.last_y+1,self.last_num+1)
        #add n+1 right
        for i in range(self.cur_ring+1):
            self.add_square(self.last_x+1,self.last_y,self.last_num+1)
        #add n+1 down
        for i in range(self.cur_ring+1):
            self.add_square(self.last_x,self.last_y-1,self.last_num+1)
           #increases by 2 because we're adding 2 squares in each direction 
        self.cur_ring = self.cur_ring + 2
        
    
    def add_square(self, x=0,y=0,num=1):
        self.grid_dict[(x,y)] = (num,False)
        self.last_x = x
        self.last_y = y
        self.last_num = num
        

