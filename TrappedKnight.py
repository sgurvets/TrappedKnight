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
#TODO group objects by crossness vs roundness


def prime(n):
     if n == 2 or n == 3: return True
     if n < 2 or n%2 == 0: return False
     if n < 9: return True
     if n%3 == 0: return False
     r = int(n**0.5)
     f = 5
     while f <= r:
           if n%f == 0: return False
           if n%(f+2) == 0: return False
           f +=6
           
     return True
 
def plot(cmap='twilight', knight=None, filename=None):
        #expects knight class to have x,y,n visited lists
            if knight == None:
                return None
        
            x = np.array(knight.x_visited)
            y = np.array(knight.y_visited)
            z = np.array([i for i in knight.n_visited])
#            z = np.array([i for i in range(len(knight.n_visited))])
        
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

            if filename == None:
                plt.show()
                plt.close()
                return None
            if filename != None:
                plt.savefig(filename, dpi = 300)
                plt.close()
                return None
                print("saved")
                print(filename)
                
class HeatMapBuilder:
    
    def __init__(self,startx=2, starty=1,endx=10,endy=10,cmap="viridis",isprime=False ):
        
        result_array = np.zeros((endx, endx))
        curx = startx
        while curx != endx:
            cury = starty
            while cury<curx:
#            cury = starty
#            while cury != curx:
                print("cur coords = "+str(curx)+"_"+str(cury))
#            filename=directory+"trappedknight_1+_nummap/"+str(curx)+"_"+str(cury)+".png"
                k = Knight(curx,cury,isprime)
                k_steps = len(k.x_visited)
                result_array[(curx-1,cury-1)]=k_steps
                result_array[(cury-1,curx-1)]=k_steps
#            result = plot(cmap,knight=k,filename=filename)
                del k
                cury=cury+1
            curx=curx+1
        print(result_array)
        plt.imshow(result_array,cmap=cmap)
        
class FracHeatMapBuilder:
    
    def __init__(self,startx=2, starty=1,endx=10,endy=10,cmap="viridis",isprime=False ):
        
        result_array = np.zeros((endx, endx))
        curx = startx
        while curx != endx:
            cury = starty
            while cury<curx:
#            cury = starty
#            while cury != curx:
                print("cur coords = "+str(curx)+"_"+str(cury))
#            filename=directory+"trappedknight_1+_nummap/"+str(curx)+"_"+str(cury)+".png"
                kprime = Knight(curx,cury,isprime=True)
                kreg = Knight(curx,cury,isprime=False)
                k_steps = len(kreg.x_visited)
                k_prime_steps = len(kprime.x_visited)
                result_array[(curx-1,cury-1)]=k_steps/k_prime_steps
                result_array[(cury-1,curx-1)]=k_steps/k_prime_steps
#            result = plot(cmap,knight=k,filename=filename)
                del kreg
                del kprime
                cury=cury+1
            curx=curx+1
        print(result_array)
        plt.imshow(result_array,cmap=cmap)
        
class DerivativeHeatMapBuilder:
    
    def __init__(self,startx=2, starty=1,endx=10,endy=10,cmap="viridis",isprime=False ):
        
        result_array = np.zeros((endx, endx))
        curx = startx
        while curx != endx:
            cury = starty
            while cury<curx:
#            cury = starty
#            while cury != curx:
                print("cur coords = "+str(curx)+"_"+str(cury))
#            filename=directory+"trappedknight_1+_nummap/"+str(curx)+"_"+str(cury)+".png"
                k = Knight(curx,cury,isprime)
                kderiv = DerivativeKnight(1,11,isprime=True,knight=k)
                k_steps = len(k.x_visited)
                k_deriv_steps = len(kderiv.x_visited)
                result_array[(curx-1,cury-1)]=k_deriv_steps
                result_array[(cury-1,curx-1)]=k_deriv_steps
#            result = plot(cmap,knight=k,filename=filename)
                del k
                del kderiv
                cury=cury+1
            curx=curx+1
        print(result_array)
        plt.imshow(result_array,cmap=cmap)


class Master:
    #sets up the simulation and builds file names
    def __init__(self, startx=1, starty=11,endx=41,endy=61,cmap="twilight",
                 directory="/Users/sgurvets/Documents/", isprime=False):
        
        #i want this to be a local function so that it cleans up its own memory
        
        def plot(cmap='twilight', knight=None, filename=None):
        #expects knight class to have x,y,n visited lists
            if knight == None:
                return None
        
            x = np.array(knight.x_visited)
            y = np.array(knight.y_visited)
#            z = np.array([i for i in knight.n_visited])
            #this actually maps the jump count, not the spiral value
            z = np.array([i for i in range(len(knight.n_visited))])
#            z = np.array(knight.cand_count)
        
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

            if filename == None:
                plt.show()
                plt.close()
                return None
            if filename != None:
                plt.savefig(filename, dpi = 300)
                plt.close()
                return None
                print("saved")
                print(filename)
                
        curx = startx
        cury = starty
        while curx != endx:
            
#            cury = starty
#            while cury != curx:
            print("cur coords = "+str(curx)+"_"+str(cury))
            filename=directory+"trappedknight_1+_nummap/"+str(curx)+"_"+str(cury)+".png"
            k = Knight(curx,cury,isprime)
            result = plot(cmap,knight=k,filename=filename)
            del k
            del result
            curx=curx+1
            cury=curx+1
            
class HexMaster:
    #sets up the simulation and builds file names
    def __init__(self, startx=1, starty=11,endx=41,endy=61,cmap="twilight",
                 directory="/Users/sgurvets/Documents/", isprime=False):
        
        #i want this to be a local function so that it cleans up its own memory
        
        def plot(cmap='twilight', knight=None, filename=None):
        #expects knight class to have x,y,n visited lists
            if knight == None:
                return None
        
            x = np.array(knight.x_visited)
            y = np.array(knight.y_visited)
            z = np.array([i for i in knight.n_visited])
            #this actually maps the jump count, not the spiral value
#            z = np.array([i for i in range(len(knight.n_visited))])
#            z = np.array(knight.cand_count)
        
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

            if filename == None:
                plt.show()
                plt.close()
                return None
            if filename != None:
                plt.savefig(filename, dpi = 300)
                plt.close()
                return None
                print("saved")
                print(filename)
                
        curx = startx
        cury = starty
        while curx != endx:
            
#            cury = starty
#            while cury != curx:
            print("cur coords = "+str(curx)+"_"+str(cury))
            filename=directory+"hexknight_1+_xy/"+str(curx)+"_"+str(cury)+".png"
            k = HexKnight(curx,cury,isprime)
            result = plot(cmap,knight=k,filename=filename)
            del k
            del result
            curx=curx+1
#            cury=(curx*2)+1
            
        

class Knight:
    #jumps around until trapped
    def __init__(self, dx=1, dy = 2, isprime=False):
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
        self.n_visited = []
        self.cand_count = []
        self.n_visited.append(1)
        self.grid = Grid()
        for j in range(self.step_max):
                    self.grid.add_ring()
                    
        self.run(isprime)
    
    def update_max_visited(self, val):
        if val > self.max_visited:
            self.max_visited = val
        
    def run(self, isprime=False):
        step = True
        while step == True:
            step = self.step(isprime)
        print("squares visited = "+str(len(self.n_visited)))
    
    def update_position(self, candidate):
        self.xpos = candidate[0]
        self.ypos = candidate[1]
        
        self.x_visited.append(candidate[0])
        self.y_visited.append(candidate[1])
        self.n_visited.append(candidate[2])
        
        
    def step(self, isprime=False):
        if isprime==True:
            candidate = self.get_primecandidate()
        if isprime==False:
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
        cur_cand_count = 0
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
                cur_cand_count +=1
                if numfalse[0] < cur_min:
                    candidate = ((i[0],i[1],numfalse[0]))
                    cur_min = numfalse[0]
        #path is at an end
        self.cand_count.append(cur_cand_count)
        if candidate == (0,0,0):
            return "end"
        return candidate
    
    def get_primecandidate(self):
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
        cur_cand_count = 0
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
                cur_cand_count +=1
                #check if value is prime
                if prime(numfalse[0])==True:
                        #if prime, check if less than cur_min
                    if numfalse[0]< cur_min:
                        candidate = ((i[0],i[1],numfalse[0]))
                        cur_min = numfalse[0]
        self.cand_count.append(cur_cand_count)
                #if cur_min is still inf (aka no candidates were prime) then go through classic get_cand
        if cur_min == float("inf"):
            for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
                numfalse = self.grid.grid_dict[i]     
                if numfalse[1]==False:
                    if numfalse[0]< cur_min:
                        candidate = ((i[0],i[1],numfalse[0]))
                        cur_min = numfalse[0]
        if candidate == (0,0,0):
                 return "end"
        return candidate
    
    
    
class HexKnight:
    #jumps around until trapped
    def __init__(self, dx=1, dy = 2, isprime=False):
        self.xstep = dx
        self.ystep = dy
        self.step_max = max(dx,dy)
        self.xstart = 0
        self.ystart = 0
        self.zstart = 0
        self.xpos = 0
        self.ypos = 0
        self.zpos = 0
        self.max_visited = 0
        self.x_visited = []
        self.y_visited = []
        self.z_visited = []
        self.n_visited = set()
        self.n_visited.add(1)
        self.grid = HexGrid()
        for j in range(self.step_max):
                    self.grid.add_ring()
                    
        self.run(isprime)     

               
    def get_holes(self):
        all_n = set(i for i in range(1,self.max_visited+1))
        holes = all_n.difference(self.n_visited)
        return holes
    
    def update_max_visited(self, val):
        if val > self.max_visited:
            self.max_visited = val
        
    def run(self, isprime=False):
        step = True
        while step == True:
            step = self.step(isprime)
        print("squares visited = "+str(len(self.n_visited)))

    def step(self, isprime=False):
        if isprime==True:
            candidate = self.get_primecandidate()
        if isprime==False:
            candidate = self.get_candidate()
        if candidate == "end":
            print("end")
            return False
        if candidate != "end":
            self.update_position(candidate)
            self.grid.update_grid_dict(candidate)
            self.update_max_visited(candidate[3])
            return True
        
    def update_position(self, candidate):
        self.xpos = candidate[0]
        self.ypos = candidate[1]
        self.zpos = candidate[2]
        
        self.x_visited.append(candidate[0])
        self.y_visited.append(candidate[1])
        self.z_visited.append(candidate[2])
        self.n_visited.add(candidate[3])
            
    def get_candidate(self):
        x = self.xpos
        y = self.ypos
        z = self.zpos
        dx = self.xstep
        dy = self.ystep

        

        #12 candidate moves on the hex board
        #https://en.wikipedia.org/wiki/Hexagonal_chess#/media/File:Glinski_Chess_Knight.svg
        cand_tuples = [(x+dx,y+dy,z-dx-dy),
                       (x+dy,y+dx,z-dx-dy),
                       (x+dx+dy,y-dx,z-dy),
                       (x+dx+dy,y-dy,z-dx),
                       (x+dy,y-dx-dy,z+dx),
                       (x+dx,y-dx-dy,z+dy),
                       (x-dx,y-dy,z+dx+dy),
                       (x-dy,y-dx,z+dx+dy),
                       (x-dx-dy,y+dx,z+dy),
                       (x-dx-dy,y+dy,z+dx),
                       (x-dy,y+dx+dy,z-dx),
                       (x-dx,y+dx+dy,z-dy)]
        candidate=(0,0,0,0)
        cur_min = float("inf")
        for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
            #grid should be infinite, so if we try to step outside
            #the boundary, add another ring
            try:
                numfalse = self.grid.grid_dict[i]
            except KeyError:
                for j in range(self.step_max):
                    self.grid.add_ring()
                numfalse = self.grid.grid_dict[i]
                
            if numfalse[1]==False:
                if numfalse[0] < cur_min:
                    candidate = (i[0],i[1],i[2],numfalse[0])
                    cur_min = numfalse[0]
        #path is at an end
        if candidate == (0,0,0,0):
            return "end"
        return candidate
    
    def get_primecandidate(self):
        x = self.xpos
        y = self.ypos
        z = self.zpos
        dx = self.xstep
        dy = self.ystep

        

        #12 candidate moves on the hex board
        #https://en.wikipedia.org/wiki/Hexagonal_chess#/media/File:Glinski_Chess_Knight.svg
        cand_tuples = [(x+dx,y+dy,z-dx-dy),
                       (x+dy,y+dx,z-dx-dy),
                       (x+dx+dy,y-dx,z-dy),
                       (x+dx+dy,y-dy,z-dx),
                       (x+dy,y-dx-dy,z+dx),
                       (x+dx,y-dx-dy,z+dy),
                       (x-dx,y-dy,z+dx+dy),
                       (x-dy,y-dx,z+dx+dy),
                       (x-dx-dy,y+dx,z+dy),
                       (x-dx-dy,y+dy,z+dx),
                       (x-dy,y+dx+dy,z-dx),
                       (x-dx,y+dx+dy,z-dy)]
        candidate=(0,0,0,0)
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
#                cur_cand_count +=1
                #check if value is prime
                if prime(numfalse[0])==True:
                        #if prime, check if less than cur_min
                    #TODO make candidate class
                    if numfalse[0]< cur_min:
                        candidate = (i[0],i[1],i[2],numfalse[0])
                        cur_min = numfalse[0]
#        self.cand_count.append(cur_cand_count)
                #if cur_min is still inf (aka no candidates were prime) then go through classic get_cand
        if cur_min == float("inf"):
            for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
            #TODO make numfalse class
                numfalse = self.grid.grid_dict[i]     
                if numfalse[1]==False:
                    if numfalse[0]< cur_min:
                        candidate = (i[0],i[1],i[2],numfalse[0])
                        cur_min = numfalse[0]
        if candidate == (0,0,0,0):
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
        self.add_hex(self.last_x, self.last_y-1,self.last_z+1,self.last_num+1)
        #add diagonally down to the left
        for i in range(self.cur_ring -1):
            self.add_hex(self.last_x-1,self.last_y,self.last_z+1,self.last_num+1)
        #add n diagonally up to the left
        for i in range(self.cur_ring):
            self.add_hex(self.last_x-1,self.last_y+1,self.last_z,self.last_num+1)
        #add n up
        for i in range(self.cur_ring):
            self.add_hex(self.last_x,self.last_y+1,self.last_z-1,self.last_num+1)
        #add n diagonally up to the right
        for i in range(self.cur_ring):
            self.add_hex(self.last_x+1,self.last_y,self.last_z-1,self.last_num+1)
        #add n down to the right
        for i in range(self.cur_ring):
            self.add_hex(self.last_x+1,self.last_y-1,self.last_z,self.last_num+1)
        #add n down
        for i in range(self.cur_ring):
            self.add_hex(self.last_x,self.last_y-1,self.last_z+1,self.last_num+1)
           #increases by 2 because we're adding 2 squares in each direction 
        self.cur_ring = self.cur_ring + 1
        
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
        #candidate is a tuple (x,y,num) mark as visited
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
        
class BranchGrid:
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
        self.clockwise = True
        
    def update_grid_dict(self, candidate):
        #candidate is a tuple (x,y,num) mark as visited
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
        
class DerivativeKnight:
    #jumps around until trapped
    def __init__(self, dx=1, dy = 2, isprime=False, knight=None):
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
        self.n_visited = []
        self.cand_count = []
        self.n_visited.append(1)
        self.grid = self.build_deriv_grid(knight)

        self.run(isprime)
                    
    def build_deriv_grid(self,knight):
        grid_dict = {}
        print('len of n')
        print(len(knight.n_visited))
        for i in range(0,len(knight.n_visited)-1):
            grid_dict[(knight.x_visited[i],knight.y_visited[i])] = (i,False)
        return grid_dict
    
    def update_grid_dict(self, candidate):
        self.grid[(candidate[0],candidate[1])]=(candidate[2],True)
    
    
    def update_max_visited(self, val):
        if val > self.max_visited:
            self.max_visited = val
        
    def run(self, isprime=False):
        step = True
        while step == True:
            step = self.step(isprime)
        print("squares visited = "+str(len(self.n_visited)))
    
    def update_position(self, candidate):
        self.xpos = candidate[0]
        self.ypos = candidate[1]
        
        self.x_visited.append(candidate[0])
        self.y_visited.append(candidate[1])
        self.n_visited.append(candidate[2])
        
        
    def step(self, isprime=False):
        if isprime==True:
            candidate = self.get_primecandidate()
        if isprime==False:
            candidate = self.get_candidate()
        if candidate == "end":
            print("end")
            return False
        if candidate != "end":
            self.update_position(candidate)
            self.update_grid_dict(candidate)
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
        cur_cand_count = 0
        for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
            try:
                numfalse = self.grid[i]
                if numfalse[1]==False:
                    cur_cand_count +=1
                    if numfalse[0] < cur_min:
                        candidate = ((i[0],i[1],numfalse[0]))
                        cur_min = numfalse[0]
            except KeyError:
                pass
                
        #path is at an end
        self.cand_count.append(cur_cand_count)
        if candidate == (0,0,0):
            return "end"
        return candidate
    
    def get_primecandidate(self):
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
        cur_cand_count = 0
        for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
            try:
                numfalse = self.grid[i]
                if numfalse[1]==False:
                    cur_cand_count +=1
                #check if value is prime
                    if prime(numfalse[0])==True:
                        #if prime, check if less than cur_min
                        if numfalse[0]< cur_min:
                            candidate = ((i[0],i[1],numfalse[0]))
                            cur_min = numfalse[0]
            except KeyError:
                pass
                
            
        self.cand_count.append(cur_cand_count)
                #if cur_min is still inf (aka no candidates were prime) then go through classic get_cand
        if cur_min == float("inf"):
            for i in cand_tuples:
            #exclude squares we've alread been to
            #self.grid_dict[(x,y)] = (num,False)
                try:
                    numfalse = self.grid[i]     
                    if numfalse[1]==False:
                        if numfalse[0]< cur_min:
                            candidate = ((i[0],i[1],numfalse[0]))
                            cur_min = numfalse[0]
                except KeyError:
                    pass
        if candidate == (0,0,0):
                 return "end"
        return candidate
        


    