# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 13:21:09 2019

@author: Administrator
"""

#coding:utf-8
#洪水填充法去除大的噪点
import numpy as np
from PIL import Image
import sys



def flood_fill_denoise(img,w,h,visited,zone_threshold,zone):
    index = 1
    for i in range(w):
        for j in range(h):
            if visited[i][j] == -1:
                if img.getpixel((i,j)) < 230:
                    dfs(i,j,img,index,visited,zone,w,h)
                    index += 1
                else:
                    visited[i][j] == 0
    
    remove_list = [0]*w*h
    for id, val in enumerate(zone):
        if val < zone_threshold:
            remove_list[id] = 1

    for i in range(w):
        for j in range(h):
            if remove_list[visited[i][j]] == 1:
                img.putpixel((i,j), 255)
            
    return img 


def dfs(x,y,img,index,visited,zone,w,h):
    #print x, y, index,w, h
    if visited[x][y] != -1:
        return
    visited[x][y] = index
    zone[index] += 1 
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    for i in range(4):
        nx = x+dx[i]
        ny = y+dy[i]
        if nx > 0 and nx < w and ny > 0 and ny < h and  visited[nx][ny] == -1:
            if img.getpixel((nx, ny)) < 230:
                dfs(nx,ny,img,index,visited,zone,w,h)
            else:
                visited[nx][ny] = 0
    return



def flood_fill(img):
    sys.setrecursionlimit(160*60)
#    visited = np.array(0)
    w=160
    h=60
    visited = np.array([-1]*w*h)
    visited.shape = (w,h)
    threshold = 230
    zone_threshold = w*h/100
    zone = [0]*w*h
    return flood_fill_denoise(img,w,h,visited,zone_threshold,zone)
    

 
def getBinaryImage(img, b=230):
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if img.getpixel((i,j)) > b:
                img.putpixel((i,j), 255)
            else:
                img.putpixel((i,j), 0)
    return img

