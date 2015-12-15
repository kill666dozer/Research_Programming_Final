# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from math import pi, atan
from matplotlib import pyplot as plt
from matplotlib import colors
from tkinter import filedialog


def load_csv():
    """Prompts the user to find a csv to load in as a np array"""
    file_path = filedialog.askopenfilename()
    data = np.loadtxt(open(file_path, "rb"), delimiter=",")
    return data


def create_uncertainties_mask(coordAmp,maxUncertainty = .3):
    """Returns a mask to be used for cleaning low-precision data"""
    xUncertainties = coordAmp.loc[:, "xUncertainty 1"::8]
    yUncertainties = coordAmp.loc[:, "yUncertainty 1"::8]
    xBools = (xUncertainties<maxUncertainty).values
    masterBools = xBools
    yBools = (yUncertainties<maxUncertainty).values
    #Find the places where the values do not match
    discrepancies = (xBools!=yBools)
    # and set them to false on masterBools
    masterBools[discrepancies]=False
    # Now reshape the mask to fit the original dataframe
    masterMask = np.repeat(masterBools,8,1)
    return masterMask
    
def make_cleaned_sigmas(coordAmp):
    """Returns a copy of the input coordAmp dataframe with low-precision data
       removed"""
    mask = create_uncertainties_mask(coordAmp)
    coordAmp.values[~mask] = np.nan
    cleanCoordAmp = pd.DataFrame(coordAmp)
    return cleanCoordAmp

def make_coordAmp_dataframe(npArray):
    """Creates a labelled dataframe for the coordAmp dataset"""
    columnNames = []
    i = 0
    for cells in npArray[0, ::8]:
        i = i+1
        columnNameCycle = ['xPos {}'.format(i), 'yPos {}'.format(i),
                           'zPos {}'.format(i), 'amplitude {}'.format(i),
                           'xUncertainty {}'.format(i),
                           'yUncertainty {}'.format(i),
                           'zUncertainty {}'.format(i),
                           'ampUncertainty {}'.format(i)]
        columnNames = columnNames+columnNameCycle
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


def make_seq_dataframe(npArray):
    """Creates a labelled dataframe for the SeqOfEvents dataset"""
    columnNames = ['Frame Index', 'Start/End', 'Track Index', 'Merge/Split']
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


def make_featIndx_dataframe(npArray):
    """Creates a labelled dataframe for the featIndx dataset"""
    columnNames = []
    i = 0
    for columns in npArray[0]:
        i = i+1
        currentName = 'Frame {}'.format(i)
        columnNames.append(currentName)
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


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
    coordinates = zip(xPositions, yPositions)
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
        
        
def plot_mean_vectors(coordAmp):
    """Plots the vectors of average motion"""
    tails = find_track_starts(coordAmp)
    heads = find_average_positions(coordAmp)
    tailArray = np.array(tails)    
    headArray = np.array(heads)
    vectors = list(headArray - tailArray)
    x,y = zip(*tails)
    u,v = zip(*vectors)
    plt.figure()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.quiver(x,y,u,v,angles='xy', scale_units='xy', scale=1)
#    ax.set_xlim([60,80])
#    ax.set_ylim([180,200])
    plt.draw()
    plt.show()


def generate_directions(coordinates):
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


def plot_vector_direction(coordAmp):
    """Plots average vector direction as color"""
    tails = find_track_starts(coordAmp)
    heads = find_average_positions(coordAmp)
    tailArray = np.array(tails)    
    headArray = np.array(heads)
    vectors = list(headArray - tailArray)
    x,y = zip(*tails)
    u,v = zip(*vectors)
    scaledDirections = np.array(generate_directions(vectors))/(2*pi)
    plt.figure()
#    ax = plt.gca()
#    ax.set_aspect('equal', adjustable='box')
#    ax.quiver(x,y,u,v,angles='xy', scale_units='xy', scale=1, color=
#              scaledDirections)
#    ax.set_xlim([60,80])
#    ax.set_ylim([180,200])
    plt.scatter(x,y,c=scaledDirections)
    plt.draw()
    plt.show()


def plot_density_heatmap(coordAmp):
    """Plots a heatmap of particle density using the average position of the
    particles"""
    average_pos = find_average_positions(coordAmp)
    xpos,ypos = zip(*average_pos)
    heatmap,xedges,yedges = np.histogram2d(ypos, xpos, bins=25)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.imshow(heatmap, extent=extent, origin = 'lower')