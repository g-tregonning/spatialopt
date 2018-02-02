# -*- coding: utf-8 -*-
"""
Version 4 
Plotting module to present the results from Genetic Algorithm
Take a Pareto Set and a list of all the solutions found

Changes:
    - Using new raster modules as we I'm writing 

Current Idea is this gonna generate a generated plot for documentation
then an interactive plot provided through pygraph in a userface

Considerations:
    - Taking the list of objective functions from the GA
        + so [fheat, fflood, fbrownfield, fdensity]
        + Represented by value based on where they are in array
        + Can get the plot label by
            # if lbl == "fheat":
                return r'$f_{heat} $'
    - Normal plots btwn pairs of objectives
        + Continue with Many Objective Pareto-optimal
        + body of solutions
        + Pareto front
        
    - Demonstration of the convergence
        + Covering this in 
        + So take the generation array
        + Calculate the length and then select 4 generations
        + Extract the pareto-fronts from each for two objectives
        + Plot

"""

import matplotlib.pyplot as plt #Allow the solutions to be plotted
import numpy as np

HeatRisk_Fit, FloodRisk_Fit, Dist_Fit, Sprawl_Fit = 0,1,2,3

"""Date Time Stamp"""
import datetime # Allows for date and time stamping of results
now = datetime.datetime.now()
day, month, year, hour, minute = str(now.day),str(now.month),str(now.year),str(now.hour),str(now.minute)
date_time_stamp = ""+day+"_"+month+"_"+year+"_"+hour+"_"+minute

def Get_PlotLabel(Obj):
    #returns the label for the axis
    if Obj == 0:
        return r'$f_{heat} $'
    elif Obj == 1:
        return r'$f_{flood} $'
    elif Obj == 2:
        return r'$f_{brownfield} $'
    elif Obj == 3:
        return r'$f_{density} $'
    elif Obj == 4:
        return r'$f_{regeneration} $'        
    elif Obj == 5:
        return r'$f_{sprawl} $'          

def Get_Label(Obj):
    #returns the label for the axis
    if Obj == 0:
        return 'fheat'
    elif Obj == 1:
        return 'fflood'
    elif Obj == 2:
        return 'fbrownfield'
    elif Obj == 3:
        return 'fdensity'
    elif Obj == 4:
        return 'fregeneration'
    elif Obj == 5:
        return 'fsprawl'

def Create_Plots(Pareto_Set, Solutions, data_folder):
    # Generate the combonations of objectives to present

    # Count the length of fitness values using the first solution in Solutions
    # as example
    Num_Objs = len(Solutions[0].fitness.values)
    
    # Array to hold these combinations of objective functions
    Obj_Comb = []
    
    # Loop through and add combos to this array
    # so for each objective function
    for x in range(0,Num_Objs):
        # combine this with each objective function after it to the
        # limit of the length
        # and this produces combinations btwn all of them
        for y in range(x+1,Num_Objs):
            combo = [x,y]
            Obj_Comb.append(combo)       
    
    
    # Loop to plot each objective comparison defined by the above list
    for x in range(0,len(Obj_Comb)):
        
        X_Axis = Obj_Comb[x][0] # The x axis in this paticular instance
        Y_Axis = Obj_Comb[x][1] # Likewise with y axis
        
        # Plot all the solutions found
        # Moved first to see if it appears underneath the MOOP results
        Sol_fit1 = [ind.fitness.values[X_Axis] for ind in Solutions]
        Sol_fit2 = [ind.fitness.values[Y_Axis] for ind in Solutions]
        plt.plot(Sol_fit1, Sol_fit2, "x", color = "green",  label = "Solutions")         
        
        # Plot Pareto Sets        
        PSet_fit1 = [ind.fitness.values[X_Axis] for ind in Pareto_Set]
        PSet_fit2 = [ind.fitness.values[Y_Axis] for ind in Pareto_Set]
        plt.plot(PSet_fit1, PSet_fit2, "o", color = "blue", label = "Many Objective Pareto-optimal Solutions")
        
        # Plot Pareto Front
        import NonDom_Sort_v2
        ObjFunc = [X_Axis, Y_Axis]
        # Need to alter this non dom sort as it is assuming a minimisation
        # So at the moment they are all minimisations for simplicity
        # Ive replaced solutions here, not sure if theres much 

        Pareto_Front = NonDom_Sort_v2.Sort(Solutions, ObjFunc)   
        
        # Writing the Pareto_Fronts found to a        
        import Write_Raster_v3 as WR      
        
        
        Raster_Folder = data_folder[:74] # takes the results folder address 
        Pareto_Front_Name =  Get_Label(X_Axis).upper()+"_against_"+Get_Label(Y_Axis).upper()
        Raster_PF_Folder = Raster_Folder+"Rasters/PF_"+Pareto_Front_Name+"/"
        import os 
        os.makedirs(Raster_PF_Folder)
        
        suffix = "PO"+(Get_Label(X_Axis)[1]).upper()+(Get_Label(Y_Axis)[1]).upper()
        WR.Write_Array(Pareto_Front,Raster_PF_Folder,suffix )
        
        # Save the found PFs to CSVs
        import Save_Results_v1 as SR  
        SR.SavetoCsv(Pareto_Front_Name, Pareto_Front, Raster_PF_Folder, suffix)
        
        
        PF_fit1 = [ind.fitness.values[X_Axis] for ind in Pareto_Front]
        PF_fit2 = [ind.fitness.values[Y_Axis] for ind in Pareto_Front]
        plt.plot(PF_fit1, PF_fit2,"-", color = "red", linewidth=3 , label = "Pareto-optimal Solutions")        


        
               
        # Set out the labels for axis
        plt.xlabel(Get_PlotLabel(X_Axis), fontsize = 20)
        plt.ylabel(Get_PlotLabel(Y_Axis),fontsize= 20)
        
        plt.savefig(data_folder+'Plot_'+Get_Label(X_Axis)+'_against_'+Get_Label(Y_Axis)+'.jpeg')
        print "Plotted ", Get_Label(X_Axis), ' against ', Get_Label(Y_Axis)
        plt.clf()    
        plt.close