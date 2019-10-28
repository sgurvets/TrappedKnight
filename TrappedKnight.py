#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:56:19 2019

@author: sgurvets
"""

import matplotlib.pyplot as plt

class Knight:
    #jumps around until trapped
    def __init__(self, dx=1, dy = 2):
        self.xstep = dx
        self.ystep = dy
        self.step_max = max(dx,dy)
        self.xstart = 0
        self.ystart = 0
        self.xpos = 0
        self.ypos = 0
        self.x_visited = []
        self.y_visited = []
        self.n_visited = []
        self.grid = Grid()
        for j in range(self.step_max):
                    self.grid.add_ring()
        
    def run(self):
        step = True
        while step == True:
            step = self.step()
        print("squares visited = "+str(len(self.n_visited)))
        plt.plot(self.x_visited, self.y_visited)
        
    def update_position(self, candidate):
        self.xpos = candidate[0]
        self.ypos = candidate[1]
        
        self.x_visited.append(candidate[0])
        self.y_visited.append(candidate[1])
        self.n_visited.append(candidate[2])
        
        
    def step(self):
        candidate = self.get_candidate()
        if candidate == "end":
            print("end")
            return False
        if candidate != "end":
            self.update_position(candidate)
            self.grid.update_grid_dict(candidate)
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
        
        
        
class Grid:
    def __init__(self):
        self.last_num = 1
        self.last_x = 0
        self.last_y = 0
        self.grid_dict = {}
        self.cur_ring=1
        self.add_square(x=0,y=0,num=1)
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
        

