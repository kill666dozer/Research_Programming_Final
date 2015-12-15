# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 09:50:03 2015

@author: galbraithlab
"""

import csvReadIn
import plottingFunctions

def main():
    print("Welcome to gTrack Analyzer. Please choose a uTrack coordAmp csv.")
    coordAmp = csvReadIn.make_coordAmp_dataframe(csvReadIn.load_csv())
    
    print("Here are all the points localized in this data set:")
    plottingFunctions.plot_points(coordAmp)
    
    print("Now, we can access these track data and plot individual tracks:")
    plottingFunctions.plot_track(coordAmp,10)   
    plottingFunctions.plot_track(coordAmp,100)
    plottingFunctions.plot_track(coordAmp,200)
    
    print("Or all the tracks together:")
    plottingFunctions.plot_all_tracks(coordAmp)
    
    print("We can also plot the average motion vectors for each track:")
    plottingFunctions.plot_mean_vectors(coordAmp)
    
    print("The colors of the above plot are arbitrary. We can also see tracks")
    print("color-coded by direction:")
    plottingFunctions.plot_vector_direction(coordAmp)
    
    print("Since we have the average position of each particle, we can")
    print("generate a heatmap of density:")
    plottingFunctions.plot_density_heatmap(coordAmp)