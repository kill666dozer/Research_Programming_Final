# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors
from tkinter import filedialog


def load_csv():
    file_path = filedialog.askopenfilename()
    data = np.loadtxt(open(file_path, "rb"), delimiter=",")
    return data


def list_uncertainties(data):
    maxUncertainty = .3
    uncertainties = []
    for row in data:
        for uncertainty in row[4::8]:
            if uncertainty < maxUncertainty:
                uncertainties.append(uncertainty)
    return uncertainties


def make_coordAmp_dataframe(npArray):
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
    columnNames = ['Frame Index', 'Start/End', 'Track Index', 'Merge/Split']
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


def make_featIndx_dataframe(npArray):
    columnNames = []
    i = 0
    for columns in npArray[0]:
        i = i+1
        currentName = 'Frame {}'.format(i)
        columnNames.append(currentName)
    infoFrame = pd.DataFrame(npArray, index=range(0, npArray.shape[0]),
                             columns=columnNames)
    return infoFrame


# def uncertainty_mask(coordAmp, uncertaintyThreshold=.3):
#    xUncertainties = coordAmp.loc[:, 'xUncertainty 1'::8]
#    yUncertainties = coordAmp.loc[:, 'yUncertainty 1'::8]
#    xMask = xUncertainties[xUncertainties < uncertaintyThreshold] = True
#    yMask = yUncertainties[yUncertainties < uncertaintyThreshold] = True

def plot_points(coordAmp):
    xValues = coordAmp.loc[:, 'xPos 1'::8]
    yValues = coordAmp.loc[:, 'yPos 1'::8]
    plt.scatter(xValues, yValues)
    plt.show()


def plot_track(coordAmp, track):
    xPositions = coordAmp.loc[track].loc['xPos 1'::8]
    yPositions = coordAmp.loc[track].loc['yPos 1'::8]
    coordinates = zip(xPositions, yPositions)
    plt.scatter(xPositions, yPositions)
    plt.plot(xPositions, yPositions)
#    plt.xlim(0,300)
#    plt.ylim(0,300)
#    plt.show()


def plot_all_tracks(coordAmp):
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
#        plt.scatter(xPositions,yPositions)
        plt.plot(xPositions, yPositions)
#    plt.xlim(50,80)
#    plt.ylim(50,80)
    plt.show()

def find_average_positions(coordAmp):
    averagePositions = []
    for track in range(1, coordAmp.shape[0]):
        xPositions = coordAmp.loc[track].loc['xPos 1'::8]
        yPositions = coordAmp.loc[track].loc['yPos 1'::8]
        averagePositions.append((xPositions.mean(),yPositions.mean()))
    return averagePositions
    
def find_track_starts(coordAmp):
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
    ax.set_xlim([60,80])
    ax.set_ylim([180,200])
    plt.draw()
    plt.show()
    