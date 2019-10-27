#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 13:56:19 2019

@author: sgurvets
"""

class Knight:
    #jumps around until trapped
    def __init__(self):
        self.xstep = 1
        self.ystep = 2
        self.xstart = 0
        self.ystart = 0
        self.xpos = 0
        self.ypos = 0
#        not collecting path now, maybe later
#        self.visited = []
        
    def step(self, grid):
        candidate = self.get_candidate(grid)
        if candidate == "end":
            print("end")
        if candidate != "end":
            self.update_position(candidate)
        
    def get_candidate(self,grid):
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
        cur_max = 0
        for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
            numfalse = grid.grid_dict[i]
            if numfalse[1]==False:
                if numfalse[0] > cur_max:
                    candidate = ((i[0],i[1],numfalse[0]))
                    cur_max = numfalse[1]
        #path is at an end
        if candidate == (0,0,0):
            return "end"
        return candidate
        
        
        
class Grid:
    def __init__(self, r = 100):
        self.last_num = 1
        self.last_x = 0
        self.last_y = 0
        self.grid_dict = {}
        self.cur_ring=1
        self.add_square(x=0,y=0,num=1)
        self.add_ring()
        self.cur_ring = 3
        
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
            
        self.cur_ring
        
    
    def add_square(self, x=0,y=0,num=1):
        self.grid_dict[(x,y)] = (num,False)
        self.last_x = x
        self.last_y = y
        self.last_num = num
