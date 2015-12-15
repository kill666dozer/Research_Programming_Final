# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 09:39:32 2015

Contains the utilities necessary to feed the plotting functions

@author: scott.breitenstein
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from math import pi, atan

def generate_directions(coordinates):
    """Takes a list of tuples representing average motion vectors and generates
       directional values in radians"""
    directions = []
    for coordinate in coordinates:
        direction = atan(coordinate[1]/coordinate[0])
        if coordinate[0] > 0:
            if coordinate[1] > 0:
                pass
            else:
                direction = direction + (2*pi)
        else:
            direction = direction + pi
        directions.append(direction)
    return directions 

def find_average_positions(coordAmp):
    """Finds the average positions of each track in a coordAmp file and returns
    them as a list of tuples"""
    averagePositions = []
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
        averagePositions.append((xPositions.mean(),yPositions.mean()))
    return averagePositions
    
def find_track_starts(coordAmp):
    """Finds the beginning positions of each track and returns them as a list 
    of tuples"""
    trackStarts = []    
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
        frame = 0
        xPosition = np.nan
        while (np.isnan(xPosition)):
            xPosition = xPositions[frame]
            frame = frame + 1
        trackStarts.append((xPositions[frame], yPositions[frame]))
    return trackStarts