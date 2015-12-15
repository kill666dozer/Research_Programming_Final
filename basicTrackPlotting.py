# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 09:39:32 2015

@author: galbraithlab
"""

import numpy as np
import pandas as pd
from math import pi, atan
from matplotlib import pyplot as plt

def plot_points(coordAmp):
    """Plots all the individual points in a coordAmp file"""
    xValues = coordAmp.loc[:, 'xPos 1'::8]
    yValues = coordAmp.loc[:, 'yPos 1'::8]
    plt.scatter(xValues, yValues)
    plt.show()


def plot_track(coordAmp, track):
    """Plots a single track from a coordAmp file"""
    xPositions = coordAmp.loc[track].loc['xPos 1'::8]
    yPositions = coordAmp.loc[track].loc['yPos 1'::8]
    plt.scatter(xPositions, yPositions)
    plt.plot(xPositions, yPositions)

def plot_all_tracks(coordAmp):
    """Plots all the tracks from a coordAmp file"""
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
        plt.plot(xPositions, yPositions)
#    plt.xlim(50,80)
#    plt.ylim(50,80)
    plt.show()

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