# -*- coding: utf-8 -*-
"""
CSVReadIn.py

This file contains the machinery for converting raw csv track data to useful 
panda dataframes. 
"""
import numpy as np
import pandas as pd
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
    coordAmpArray = coordAmp.values
    coordAmpArray[~mask] = np.nan
    cleanCoordAmp = make_coordAmp_dataframe(coordAmpArray)
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
        
        
