# -*- coding: utf-8 -*-
"""
Version 1
Plotting module to present the results from Genetic Algorithm
Take a Pareto Set and a list of all the solutions found

NOTES
+ Need to sort out extracting the Pareto front
    - Getting some weird results

"""

from copy import copy # allow to copy arrays
import matplotlib.pyplot as plt #Allow the solutions to be plotted
import numpy as np

HeatRisk_Fit, FloodRisk_Fit, Dist_Fit, Sprawl_Fit = 0,1,2,3

"""Date Time Stamp"""
import datetime # Allows for date and time stamping of results
now = datetime.datetime.now()
day, month, year, hour, minute = str(now.day),str(now.month),str(now.year),str(now.hour),str(now.minute)
date_time_stamp = ""+day+"_"+month+"_"+year+"_"+hour+"_"+minute

def Get_Label(Obj):
    #returns the label for the axis
    if Obj == 0:
        return r'$f_{heat} $'
    elif Obj == 1:
        return r'$f_{flood} $'
    elif Obj == 2:
        return r'$f_{brownfield} $'
        
    elif Obj == 3:
        return r'$f_{density} $'

def Create_Plots(Pareto_Set, Solutions):
    # Format   

    
    Obj_Comb = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    
    # Loop to plot each objective comparison defined by the above list
    for x in range(0,len(Obj_Comb)):
        
        X_Axis = Obj_Comb[x][0] # The x axis in this paticular instance
        Y_Axis = Obj_Comb[x][1] # Likewise with y axis
        
        # Plot Pareto Sets        
        PSet_fit1 = [ind.fitness.values[X_Axis] for ind in Pareto_Set]
        PSet_fit2 = [ind.fitness.values[Y_Axis] for ind in Pareto_Set]
        plt.plot(PSet_fit1, PSet_fit2, "o", color = "blue", label = "Many Objective Pareto-optimal Solutions")
        
        # Plot Pareto Front
        import NonDom_Sort_v1
        ObjFunc = [X_Axis, Y_Axis]
        # Need to alter this non dom sort as it is assuming a minimisation
        Pareto_Front = NonDom_Sort_v1.Sort(Pareto_Set, ObjFunc)   
        
        PF = np.array(Pareto_Front)
            
        #PFrnt_fit1 = [ind.fitness.values[X_Axis] for ind in Pareto_Front]
        #PFrnt_fit2 = [ind.fitness.values[Y_Axis] for ind in Pareto_Front]
        plt.plot(PF[:,X_Axis], PF[:,Y_Axis],"-", color = "red", linewidth=2 , label = "Pareto-optimal Solutions")        

        # Plot all the solutions found
        Sol_fit1 = [ind.fitness.values[X_Axis] for ind in Solutions]
        Sol_fit2 = [ind.fitness.values[Y_Axis] for ind in Solutions]
        plt.plot(Sol_fit1, Sol_fit2, "x", color = "green",  label = "Solutions") 
        
               
        # Set out the labels for axis
        plt.xlabel(Get_Label(X_Axis), fontsize = 20)
        plt.ylabel(Get_Label(Y_Axis),fontsize= 20)
        
        data_folder = 'C:/Users/danie_000/Python_Codes/London_Case_Study/Results/'
        plt.savefig(data_folder+'Plot_'+str(X_Axis)+'_against_'+str(Y_Axis)+'_'+date_time_stamp+'.jpeg')
        print "Plotted Objective ", X_Axis, ' against ', Y_Axis
        plt.clf()    
        plt.close
    

        

def Plot(Pareto_Set, ManyObj_Pareto, Solutions, CDT, X_Axis, Y_Axis):
    data_folder = 'C:/Users/danie_000/Python_Codes/Journal_Article_Code/Results/PhD_Seminar/'
    plt.savefig(data_folder+'Plot_'+X_Axis+'_against_'+Y_Axis+'_'+date_time_stamp+'.jpeg')
    print "Plotted Objective ", X_Axis, ' against ', Y_Axis
    plt.clf()    
    plt.close
    