# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 01:27:16 2024
@author: oscar
"""
from pathlib import Path
import cv2 

from queens_solver import QueensSolver
from queens_parser import parse_queens_img, draw_queens_board

for f in Path('examples', 'inputs').glob('*'):
    img = cv2.imread(f)
    
    board, img, rows, cols = parse_queens_img(img)
    Q = QueensSolver(depth=2).solve(board)    
    answer = draw_queens_board(img, Q, rows, cols)
    
    answer_filepath = Path('examples', 'outputs', f'answer_{f.name}')
    cv2.imwrite(answer_filepath, answer)
