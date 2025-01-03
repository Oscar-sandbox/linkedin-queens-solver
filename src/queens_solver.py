# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 22:45:52 2024

@author: oscar
"""
from copy import deepcopy
import numpy as np


class QueensSolver:
    
    def __init__(self, depth): 
        ''' Construct a Queens solver using backtracking.'''
        self.depth = depth
        
        
    def check_Q(self):
        ''' Check if self.Q contains an answer for the puzzle.'''
        if np.count_nonzero(self.Q) != self.N: return False # all queens placed.
        if np.any(np.count_nonzero(self.Q, 0) > 1): return False # valid columns.
        if np.any(np.count_nonzero(self.Q, 1) > 1): return False # valid rows.
        if np.any(np.count_nonzero(self.Q & self.G, (1,2)) > 1): return False # valid colors.
        return True
    
    
    def check_X(self): 
        ''' Check if self.X has any immediate contradictions.'''
        if np.any(~np.any(self.Q, 0) & np.all(self.X, 0)): return False # valid columns.
        if np.any(~np.any(self.Q, 1) & np.all(self.X, 1)): return False # valid rows.
        
        xg_count = np.count_nonzero(self.X & self.G, (1,2))
        qg_bool = np.any(self.Q & self.G, (1,2))          
        if np.any(~qg_bool & (xg_count == self.G_count)): return False # valid colors.
        
        return True


    def update_Q(self, i, j):
        ''' Add a new queen at (i,j) and update self.X.'''
        self.Q[i,j] = True # add queen.
        
        self.X[:,j] = True # mark column.
        self.X[i] = True # mark row.
        
        e = self.N-1
        self.X[max(i-1,0), max(j-1,0)] = True # mark diagonals.
        self.X[max(i-1,0), min(j+1,e)] = True
        self.X[min(i+1,e), max(j-1,0)] = True
        self.X[min(i+1,e), min(j+1,e)] = True
        
        self.X[self.B == self.B[i,j]] = True # mark colors.
    
    
    def find_trivial_row(self): 
        ''' Find a pair (i,j), if existent, where a queen completes a row.'''
        xg_count = np.count_nonzero(self.X, 1)
        qg_bool = np.any(self.Q, 1)    
        i = np.nonzero(~qg_bool & (xg_count == self.N-1))[0]
        
        if i.size: 
            i = i[0]
            return i, np.nonzero(~self.X[i])[0][0]
     
        
    def find_trivial_col(self): 
        ''' Find a pair (i,j), if existent, where a queen completes a column.'''
        xg_count = np.count_nonzero(self.X, 0)
        qg_bool = np.any(self.Q, 0)    
        j = np.nonzero(~qg_bool & (xg_count == self.N-1))[0]
        
        if j.size: 
            j = j[0]
            return np.nonzero(~self.X[:,j])[0][0], j
    
    
    def find_trivial_group(self): 
        ''' Find a pair (i,j), if existent, where a queen completes a color.'''
        xg_count = np.count_nonzero(self.X & self.G, (1,2))
        qg_bool = np.any(self.Q & self.G, (1,2))  
        g = np.nonzero(~qg_bool & (xg_count == self.G_count-1))[0]
        
        if g.size: 
            g = g[0]
            i, j = np.nonzero(self.G[g] & ~self.X)
            return i[0], j[0]
    
    
    def fill_trivials(self):
        ''' Recursively fill every possible position where a queen would 
        complete a row, a column or a color. '''
        find_trivials = [
            self.find_trivial_group,
            self.find_trivial_row, 
            self.find_trivial_col
        ]
        
        for find_trivial in find_trivials: 
            pos = find_trivial()
            if pos:
                self.update_Q(*pos)
                self.fill_trivials()
       
        
    def solve_rec(self, depth): 
        ''' Recursion function for solving the puzzle with backtracking.'''
        self.fill_trivials()
        if self.check_Q(): return True
        if not depth: return False

        for i in range(self.N):
            for j in range(self.N):
                branch = deepcopy(self)
                branch.update_Q(i, j)
                
                if not branch.check_X():
                    self.X[i,j] = True
                else:
                    if branch.solve_rec(depth-1):
                        self.Q, self.X = branch.Q, branch.X
                        return True
    
    
    def solve(self, B):
        ''' Solve the Queens puzzle given by an NxN board.'''
        self.B = B # board.
        self.N = len(B)
          
        self.G = np.array([B == g for g in range(self.N)]) # board mask for each color. 
        self.G_count = np.count_nonzero(self.G, (1,2)) # number of cells for each color. 
        
        self.Q = np.zeros_like(B, dtype=bool) # current queens.
        self.X = np.zeros_like(B, dtype=bool) # current marks.
        
        if self.solve_rec(depth=self.depth): 
            return self.Q