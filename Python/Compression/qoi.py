"""
Python implementation of the QOI formatting algorithm wich is faster than PNG and has a slightly lower compression rate.

references : https://qoiformat.org/qoi-specification.pdf
             https://www.youtube.com/watch?v=EFUYNoFRHQI
"""

from PIL import Image
from numpy import asarray
import cv2

def hash_index(r, g, b, a=0):
    return (r * 3 + g * 5 + b * 7 + a * 11) % 64

def linearize_channel(channel):
    output = []
    for row in channel:
        output.extend(row)
    return output

def linearize_img(img):
    return [linearize_channel(channel) for channel in img]

# img = [[[1, 1],
#         [3, 4]], 
       
#        [[2, 2],
#         [7, 8]], 
       
#        [[3, 3], 
#         [6, 8]]
#        ]

def qoi(img):
    # width, height, channel_nb = len(img[0][0]), len(img[0]), len(img)
    img = linearize_img(img)
    
    array = [0] * 64
    
    previous = [0, 0, 0]
    run_length = 0
    blocks = []
    
    for r, g, b in zip(*img):
        prev_r = previous[0]
        prev_g = previous[1]
        prev_b = previous[2]
        
        if r == prev_r and g == prev_g and b == prev_b: # QOI_OP_RUN
            run_length += 1
            if run_length == 62:
                run_length = 0
                blocks.append(192 | 61)
            continue
        
        if run_length != 0:
            run_length = 0
            blocks.append(192 | run_length-1)
            
        i = hash_index(r, g, b)
        if array[i] == (r, g, b): # QOI_OP_INDEX
            blocks.append(i)
            continue
        array[i] = (r, g, b)
            
        dr = r - prev_r
        dg = g - prev_g
        db = b - prev_b
        
        if -2 <= dr <= 1 and -2 <= dg <= 1 and -2 <= db <= 1: # QOI_OP_DIFF
            blocks.append(64 | dr << 4 | dg << 2 | db)
            continue
            
        if -32 <= dg <= 31 and -8 <= dr - dg <= 7 and -8 <= db - dg <= 7: # QOI_OP_LUMA
            blocks.extend((128 | dg + 32, (dr - dg + 8) << 4 | (db - dg + 8)))
            continue
        
        # QOI_OP_RGB
        blocks.extend((254, r, g, b))
            
        previous = [r, g, b]
    return blocks
    
img = Image.open("clover.png")
data = asarray(img)
print(data.shape)
b, g, r = cv2.split(data)

res = qoi([r, g, b])
print(res, len(res))
print(len(r) + len(g) + len(b))