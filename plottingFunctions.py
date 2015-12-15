# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 09:41:51 2015

Contains all the plotting functions for graphical output

@author: scott.breitenstein
"""
import trackManipulations
import numpy as np
import pandas as pd
from math import pi, atan
from matplotlib import pyplot as plt

def plot_points(coordAmp):
    """Plots all the individual points in a coordAmp file"""
    xValues = coordAmp.loc[:, 'xPos 1'::8]
    yValues = coordAmp.loc[:, 'yPos 1'::8]
    plt.clf()
    plt.scatter(xValues, yValues)
    plt.show()


def plot_track(coordAmp, track):
    """Plots a single track from a coordAmp file"""
    xPositions = coordAmp.loc[track].loc['xPos 1'::8]
    yPositions = coordAmp.loc[track].loc['yPos 1'::8]
    plt.clf()
    plt.scatter(xPositions, yPositions)
    plt.plot(xPositions, yPositions)
    plt.show()

def plot_all_tracks(coordAmp):
    """Plots all the tracks from a coordAmp file"""
    plt.clf()
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
        plt.plot(xPositions, yPositions)
#    plt.xlim(50,80)
#    plt.ylim(50,80)
    plt.show()

def plot_mean_vectors(coordAmp):
    """Plots the vectors of average motion"""
    tails = trackManipulations.find_track_starts(coordAmp)
    heads = trackManipulations.find_average_positions(coordAmp)
    tailArray = np.array(tails)    
    headArray = np.array(heads)
    vectors = list(headArray - tailArray)
    x,y = zip(*tails)
    u,v = zip(*vectors)
    plt.clf()
    plt.figure()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.quiver(x,y,u,v,angles='xy', scale_units='xy', scale=1)
#    ax.set_xlim([60,80])
#    ax.set_ylim([180,200])
#    plt.draw()
    plt.show()   


def plot_vector_direction(coordAmp):
    """Plots average vector direction as color"""
    tails = trackManipulations.find_track_starts(coordAmp)
    heads = trackManipulations.find_average_positions(coordAmp)
    tailArray = np.array(tails)    
    headArray = np.array(heads)
    vectors = list(headArray - tailArray)
    x,y = zip(*tails)
    u,v = zip(*vectors)
    directions = trackManipulations.generate_directions(vectors)
    scaledDirections = np.array(directions)/(2*pi)
    plt.clf()
    plt.figure()
    plt.scatter(x,y,c=scaledDirections)
    plt.draw()
    plt.show()


def plot_density_heatmap(coordAmp):
    """Plots a heatmap of particle density using the average position of the
    particles"""
    average_pos = trackManipulations.find_average_positions(coordAmp)
    xpos,ypos = zip(*average_pos)
    plt.clf()
    heatmap,xedges,yedges = np.histogram2d(ypos, xpos, bins=25)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap, extent=extent, origin = 'lower')