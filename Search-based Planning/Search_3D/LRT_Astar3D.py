# this is the three dimensional N>1 LRTA* algo
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: yue qi
"""
import numpy as np
import matplotlib.pyplot as plt

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../Search-based Planning/")
from Search_3D.env3D import env
from Search_3D import Astar3D
from Search_3D.utils3D import getDist, getRay, StateSpace, Heuristic, getNearest, isCollide, hash3D, dehash, \
    cost, obstacleFree
from Search_3D.plot_util3D import visualization
import queue

class LRT_A_star2:
    def __init__(self, resolution=0.5, N=7):
        self.N = N
        self.Astar = Astar3D.Weighted_A_star(resolution=resolution)
        self.path = []

    def updateHeuristic(self):
        # Initialize hvalues at infinity
        for strxi in self.Astar.CLOSED:
            self.Astar.h[strxi] = np.inf
        Diff = True
        while Diff:  # repeat DP until converge
            hvals, lasthvals = [], []
            for strxi in self.Astar.CLOSED:
                xi = dehash(strxi)
                lasthvals.append(self.Astar.h[strxi])
                # update h values if they are smaller
                Children = self.Astar.children(xi)
                minfval = min([cost(xi, xj, settings=0) + self.Astar.h[hash3D(xj)] for xj in Children])
                # h(s) = h(s') if h(s) > c(s,s') + h(s') 
                if self.Astar.h[strxi] >= minfval:
                    self.Astar.h[strxi] = minfval
                hvals.append(self.Astar.h[strxi])
            if lasthvals == hvals: Diff = False

    def move(self):
        strst = self.Astar.x0
        st = self.Astar.start
        ind = 0
        # find the lowest path down hill
        while strst in self.Astar.CLOSED:  # when minchild in CLOSED then continue, when minchild in OPEN, stop
            # strChildren = self.children(st)
            strChildren = [hash3D(i) for i in self.Astar.children(st)]
            minh, minchild = np.inf, None
            for child in strChildren:
                h = self.Astar.h[child]
                if h <= minh:
                    minh, minchild = h, dehash(child)
            self.path.append([st, minchild])
            strst, st = hash3D(minchild), minchild
            for (_, strp) in self.Astar.OPEN.enumerate():
                if strp == strst:
                    break
            ind += 1
            if ind > 1000:
                break
        self.Astar.reset(st)

    def run(self):
        while True:
            if self.Astar.run(N=self.N):
                self.Astar.Path = self.Astar.Path + self.path
                self.Astar.done = True
                visualization(self.Astar)
                plt.show()
                break
            self.updateHeuristic()
            self.move()


if __name__ == '__main__':
    T = LRT_A_star2(resolution=0.5, N=150)
    T.run()
