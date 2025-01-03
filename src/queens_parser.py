# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 00:29:20 2024

@author: oscar
"""

import numpy as np
from scipy.signal import find_peaks
import cv2


def parse_queens_img(img):
    ''' Parses an image representation of a board into a NxN numpy array.'''
    img = img.copy()
    
    # Crop the image to isolate the board. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    x, y, dx, dy = cv2.boundingRect(contour)
    
    assert 0.95 < dy/dx < 1.05, 'Could not detect square board'
    img = img[y:y+min(dx,dy), x:x+min(dx,dy)]
    
    # Detect the number of queens by inspecting the borders between cells. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    
    binary_rows = np.count_nonzero(binary, 1)
    binary_cols = np.count_nonzero(binary, 0)
    
    rows, _ = find_peaks(binary_rows, height=2*np.median(binary_rows), distance=10)
    cols, _ = find_peaks(binary_cols, height=2*np.median(binary_cols), distance=10)
    
    assert len(rows) == len(cols), 'Could not detect rows and columns'
    N = len(rows) - 1
    
    # Calculate the median color per cell. 
    colors = np.zeros((N, N, 3), dtype=np.float32)
    for i in range(N):
        for j in range(N):
            cell = img[rows[i]:rows[i+1], cols[j]:cols[j+1]]
            colors[i,j] = np.median(cell, (0,1))
    
    # Cluster the cell colors into N groups, coded with numbers 0 to N-1. 
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)
    _, labels, _ = cv2.kmeans(colors.reshape(N**2,3), N, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    
    board = labels.reshape(N, N)
    return board, img, rows, cols
    
def draw_queens_board(img, Q, rows, cols):
    ''' Draws the solution of the puzzle Q on top of an image.'''
    img = img.copy()
    
    for i,j in zip(*np.nonzero(Q)):
        hx = (rows[i] + rows[i+1]) // 2
        hy = (cols[j] + cols[j+1]) // 2
        rho = min(rows[i+1] - rows[i], cols[j+1] - cols[j]) // 5
        cv2.circle(img, (hy, hx), rho, (0,0,0), cv2.FILLED, cv2.LINE_AA)
     
    return img 
        