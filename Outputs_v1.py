# -*- coding: utf-8 -*-
"""
Outputs version 1

Module to handle the outputs of the Genetic Algorithm search over London
"""

import NonDom_Sort_v3 as NonDom_Sort
import Initialise_v3 as Init

import numpy as np
from copy import copy
from itertools import combinations
import os 
import matplotlib.pyplot as plt #Allow the solutions to be plotted
# Facilitate the creation of a datetime stamp for the results
import datetime, time 
import rasterIO

# Creating a data time stamp
start_time = time.time()
date_time_stamp = datetime.datetime.fromtimestamp(start_time).strftime('%d%m%y-%H%M')

def Get_Label(Obj):
    #returns the label for the axis
    if Obj   == 0:  return r'$f_{heat} $'
    elif Obj == 1:  return r'$f_{flood} $'
    elif Obj == 2:  return r'$f_{dist} $'
    elif Obj == 3:  return r'$f_{brownfield} $'
    elif Obj == 4:  return r'$f_{sprawl} $'
    elif Obj == 5:  return r'$f_{greenspace} $'
    
def Get_String(Obj):
    if Obj   == 0:  return 'fheat'
    elif Obj == 1:  return 'fflood'
    elif Obj == 2:  return 'fdist'
    elif Obj == 3:  return 'fbrownfield'
    elif Obj == 4:  return 'fsprawl'
    elif Obj == 5:  return 'fgreenspace'
    elif Obj == True: return 'Solutions'
    
def Return_Per_Retention():
    Dwell_Constraint_list   = np.loadtxt("Dwell_Constraint.txt",delimiter=",")
    Ptal_Constraint_list    = np.loadtxt("PTAL_Constraint.txt",delimiter=",")
    
    Av_Dwell_Retention  = np.sum(Dwell_Constraint_list)/ len(Dwell_Constraint_list)
    Av_Ptal_Retention   = np.sum(Ptal_Constraint_list) / len(Ptal_Constraint_list)
    
    return Av_Dwell_Retention, Av_Ptal_Retention

def Output_Run_Details(Results_Folder, Modules, Operators, Prob_Form, GA_Parameters,Fitnesses):
    # Function to output a text file detailing the parameters for the GA Search
    # Including:
        # + Data time stamp
        # + Modules used (so can see which versions were used)
        # + How the problem is formulated (Dwelling totals)
        # + The objectives optimised 
        # + Operators used for the evolutionary operating
        #      @   

    OutFile = open(Results_Folder+'Output_file.txt', 'w')
    OutFile.write('Genetic Algorithm Run over London Case Study\n')
    
    OutFile.write('Run completed on '+date_time_stamp+'\n')  
    
    # Write the modules used
    OutFile.write('Modules Utilised\n')
    for x in range(0, len(Modules), 2):
        OutFile.write(Modules[x]+': '+Modules[x+1]+'\n')
    
    # Write the parameters for the problem being solved
    OutFile.write('Problem Formulation\n')
    for x in range(0,len(Prob_Form),2):
        OutFile.write(Prob_Form[x]+': '+str(Prob_Form[x+1])+'\n')    
    
    # Write the objective functions optimised
    OutFile.write('Objectives Optimised\n')
    for x in range(0, len(Fitnesses)):
        OutFile.write(Fitnesses[x]+' ')
    OutFile.write('\n')
    
    # Write the operators used
    OutFile.write('Operators Utilised\n')    
    for x in range(0, len(Operators),2):
        OutFile.write(Operators[x]+': '+Operators[x+1]+'\n')
    
    # Writing the retention rate of the constraints
    Av_Dwell_Retention, Av_Ptal_Retention = Return_Per_Retention()
    OutFile.write('Average retention rate after Dwelling Total Restraint is '+str(Av_Dwell_Retention)+'%\n')
    
    # Only writing if its been utilised
    if Av_Ptal_Retention > 0:
        OutFile.write('Average retention rate after PTAL Restraint is '+str(Av_Ptal_Retention)+'%\n')
    
    # Write the search parameters for the Genetic Algorithm
    OutFile.write('GA Search Parameters\n')    
    for x in range(0, len(GA_Parameters),2):
        OutFile.write(GA_Parameters[x]+': '+str(GA_Parameters[x+1])+'\n')

    OutFile.close()
    
    print "Written Run Details File"

            
def Normalise_MinMax(Sol_List):
    # Function calculates the maximum and minimum value for each     
    MinMax_list = []
    
    # Calculate the number of objectives to calculate min and maxs for
    # by calculatng the length of the first solutions fitness column
    No_Obj = len(Sol_List[0][2])
    
    # For each Obj calculate their minimum and maximum and add them to
    # the MinMax_list
    for ObjFunc in range(0, No_Obj):

        # Sort the solution list ascending by the objective         
        Sol_List.sort(key=lambda x: x[2][ObjFunc], reverse = False) #currently sorted by smallest 1st obj    
        # Extract the minimum solution        
        Obj_Min = Sol_List[0][2][ObjFunc]    
        Sol_List.sort(key=lambda x: x[2][ObjFunc], reverse = True) #currently sorted by smallest 1st obj    
        Obj_Max = Sol_List[0][2][ObjFunc]     
        MinMax = (Obj_Min,Obj_Max)
        MinMax_list.append(MinMax)
        
    return MinMax_list
    
def Format_Solutions(Solutions):
    # Function formats the GA outputs into a form which can  be normalised 
    # and plottted.
    
    # Array to hold the new formatted solutions
    Frmt_Sols = []
    
    # Solution number count
    Sol_num = 0    
    
    for Sol in Solutions:
        
        fitnesses = []
        for Obj_Function in Sol.fitness.values:
            fitnesses.append(Obj_Function)
        frmt_sol = [Sol_num, Sol, fitnesses]
        Frmt_Sols.append(frmt_sol)
        Sol_num +=1
    return Frmt_Sols

def Normalise_Solutions(MinMax_list, Solutions):
    
    Copied_Solutions = copy(Solutions)
    Norm_List = []
    
    for solution in Copied_Solutions:
        new_solution = []
        new_solution.append(solution[0])
        new_solution.append(solution[1])
        Norm_Fitnesses = []
        for a in range(0, len(solution[2])):
            # Normalise the fitness using the Minimum and Maximum from the MinMax_list
            Min, Max = MinMax_list[a][0], MinMax_list[a][1]
            Norm_Obj = Norm(solution[2][a], Min, Max)
            Norm_Fitnesses.append(Norm_Obj)

        new_solution.append(Norm_Fitnesses)

        Norm_List.append(new_solution)
    
    return Norm_List
    
    
def Norm(value, Obj_Min, Obj_Max):
    Norm_value = (value - Obj_Min)/(Obj_Max - Obj_Min)
    return Norm_value

def frmt_CSV(Set):
    Copied_Set = copy(Set)
    New_Set= []
    for solution in Copied_Set:
        new_solution = []
        new_solution.append(solution[0])
        ObjFunc = np.array(solution[2])
        for x in ObjFunc:
            new_solution.append(x)
        New_Set.append(new_solution)
    New_Set=np.array(New_Set)
    return New_Set
    
def Save_to_CSV(Set, Obj_list, Norm, Results_Folder):
    Output_File = 'PO_Set_'
    if Norm == True:
        Output_File += 'Norm_'
    for Obj in Obj_list:
        Obj_String  = str(Get_String(Obj))
        Output_File = Output_File+Obj_String+'_'
    frmt_Set = frmt_CSV(Set)
    File = str(Results_Folder)+str(Output_File)+"_Fitness.csv"
    
    np.savetxt(File, frmt_Set,  delimiter=',', newline='\n')
    
    
    
def Save_Pareto_Set(PO_Set, Obj_list, Norm, Results_Folder):
    Output_File = 'PO_Set_'
    if Norm == True:
        Output_File += 'Norm_'
    for Obj in Obj_list:
        Obj_String  = str(Get_String(Obj))
        Output_File = Output_File+Obj_String+'_'
    
    f = open(Results_Folder+Output_File+".txt",'w')
    for sol in PO_Set:
        f.write(str(sol)+'\n')
    f.close()

def Plot_Format(Set):
    Copied_Set = copy(Set)
    New_Set= []
    for solution in Copied_Set:
        new_solution = []
        ObjFunc = np.array(solution[2])
        for x in ObjFunc:
            new_solution.append(x)
        New_Set.append(new_solution)
    New_Set=np.array(New_Set)
    return New_Set    
    
def Plot(Pareto_Set, MOPO, Solutions, X_Axis, Y_Axis, Results_Folder, Norm):
    # Format it to a numpy array type so [:, Axis] works
    # Returns in the form [SolNum Obj1, Obj2, ...]
    Pareto_Set  = Plot_Format(Pareto_Set)
    MOPO        = Plot_Format(MOPO)
    Solutions   = Plot_Format(Solutions)
    
    # Plot Solutions, Pareto set, multi obj Pareto set and current development trend
    plt.plot(Solutions[:,X_Axis],Solutions[:,Y_Axis], "x", color = "green", markersize=5, label = "Solutions")    
    #plt.plot(Pareto_Set[:,X_Axis],Pareto_Set[:,Y_Axis], "-", color = "red", markersize=15, label = "Pareto-optimal Solutions")   
    #plt.plot(MOPO[:,X_Axis],MOPO[:,Y_Axis], "o", color = "blue", markersize=8, label = "Many Objective Pareto-optimal Solutions")
    #plt.plot(CDT[:,X_Axis],CDT[:,Y_Axis], "^", color = "yellow", markersize=12, label = "Council's Proposed Development Plan")   
    plt.plot(Pareto_Set[:,X_Axis],Pareto_Set[:,Y_Axis], "-", color = "red", linewidth=2 , label = "Pareto-optimal Solutions")   
       
    X_Axis_label = Get_Label(X_Axis)
    Y_Axis_label = Get_Label(Y_Axis)
    
    #plt.title("Non Dominated front of a set solutions")
    plt.xlabel(X_Axis_label, fontsize = 20)
    plt.ylabel(Y_Axis_label,fontsize= 20)
    
    #plt.legend(loc=1)
    X_Axis, Y_Axis = Get_String(X_Axis), Get_String(Y_Axis)
    
    
   
    if Norm == True:
        Output_File = Results_Folder+'Norm_Plot_'+X_Axis+'_against_'+Y_Axis+'_'+date_time_stamp+'.jpeg'        
    else:
         Output_File = Results_Folder+'Plot_'+X_Axis+'_against_'+Y_Axis+'_'+date_time_stamp+'.jpeg'
    
    plt.savefig(Output_File)
    print "Plotted Objective ", X_Axis, ' against ', Y_Axis
    plt.clf()    
    plt.close    
    

        
def New_Results_Folder(Results_Folder):
    # Function to create a new folder within the results folder to handle the 
    # results of the specific run
    
    # Location of the new folder with 'Run' and the data time stamp attached
    New_Results_Folder = Results_Folder+'Run_'+date_time_stamp+'/'
      
    # Check it doesn't already exists and then makes it a new directory
    if not os.path.exists(New_Results_Folder): os.makedirs(New_Results_Folder)  
    
    return New_Results_Folder

def Write_Rasters(Set, Results_Folder, Data_Folder, Site_Hectares):
    # Upload the details in order to save our output files  
    file_pointer        = rasterIO.opengdalraster(Data_Folder+'Empty_DevPlan.tif')       
    driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
    # Specifying the format as OSGB 1936 
    epsg = 27700
    print len(Set)
    for Solution in Set:
        # Extract the solution number
        Sol_Num = Solution[0]
        
        # Create the DevPlan and DwellPlan
        # NOTE sending Solution[1] as that is what contains the proposed sites
        DevPlan     = Init.Generate_London_DevPlan(Solution[1], Data_Folder)
        DwellPlan   = Init.Generate_London_DwellPlan(Solution[1], Data_Folder, Site_Hectares)
        
        DevPlan_Outfile     = Results_Folder+'DevPlan'+str(Sol_Num)+'.tif'
        DwellPlan_Outfile   = Results_Folder+'DwellPlan'+str(Sol_Num)+'.tif'

        rasterIO.writerasterbands(DevPlan_Outfile, 'GTiff', XSize, YSize, geo_t_params, epsg, None, DevPlan)
        rasterIO.writerasterbands(DwellPlan_Outfile, 'GTiff', XSize, YSize, geo_t_params, epsg, None, DwellPlan)
        
def Extract_ParetoFront_and_Plot(Solutions, Norm, Results_Folder, Data_Folder,Site_Hectares):
    # Function which takes the list of solutions output by the GA and extracts
    # the MOPOs as well as the PF between pairs of solutions before outputting
    # them into a csv file and plotting them.
    
    # Extract a length of the objecties from the first solution
    No_Obj = len(Solutions[0][2])
    
    
    # Create a folder within the result folder for raster datafiles
    Raster_Results_Folder = Results_Folder+'Rasters/'    
    if not os.path.exists(Raster_Results_Folder): os.makedirs(Raster_Results_Folder) 
    
    # EXTRACT MOPOS  

    # Create a list of all the obj functions
    Obj_Functions = range(0,No_Obj)
    
    # Extract the Pareto optimal set for MOPOs    
    MOPOs = NonDom_Sort.Sort(Solutions, Obj_Functions)
    Save_Pareto_Set(MOPOs, Obj_Functions,Norm,  Results_Folder)
    Save_to_CSV(MOPOs, Obj_Functions, Results_Folder, Norm)    
    
    # Extract the PF sets between     
    PF_Comb_list = list(combinations(Obj_Functions, 2))
    
    ' Write the solutions list to a csv' 
    Save_to_CSV(Solutions, Obj_Functions, Norm, Results_Folder)    
    
    for PF in PF_Comb_list:
        PO_PF = NonDom_Sort.Sort(Solutions, PF)
        print 'The length of Pareto Front between ', Get_String(PF[0]),' and ',Get_String(PF[1]),' is ',len(PO_PF)
        Save_Pareto_Set(PO_PF, PF, Norm, Results_Folder)
        Plot(PO_PF, MOPOs, Solutions, PF[0], PF[1], Results_Folder, Norm)
        Save_to_CSV(PO_PF, PF, Norm, Results_Folder)
        
        # Writing solutions of the Pareto front to rasters
        # There are too many MOPOs        
        Write_Rasters(PO_PF, Raster_Results_Folder, Data_Folder, Site_Hectares)
    # WRITE THE RESULTING RASTER FILES
    

    
    
    
def Extract_Generation_Pareto_Fronts(Generations,MinMax_list, Results_Folder, Data_Folder, Site_Hectares):
    # Module intended to generate the Pareto front of each generation of the
    # Genetic Algorithm run to display how the front converges. So idea is to
    # generate a new folder for the generations within the results folder, 
    # then a folder for each generation and save the PF in CSVs
    
    # Define a new folder within the results folder to hold the 
       
    Generations_Results_Folder = Results_Folder+'Generations/'
    
    # Generate the generations results folder 
    if not os.path.exists(Generations_Results_Folder): os.makedirs(Generations_Results_Folder)
    for gen in Generations:
        print "tl"
        print len(gen)
    # Now for each generations
    Gen_count = 0
    for Gen in Generations:
        print "Processing Generation ", Gen_count
        # Define the folder to save each paticular generation to and create it
        Each_Generations_Results_Folder = Generations_Results_Folder+'Generation_'+str(Gen_count)+'/'
        if not os.path.exists(Each_Generations_Results_Folder): os.makedirs(Each_Generations_Results_Folder)

        # Normalise the generation
        Normalised_Gen = Normalise_Solutions(MinMax_list, Gen)
        
        # Extract the Pareto fronts of this generations and save to csvs
        Extract_ParetoFront_and_Plot(Gen, False, Each_Generations_Results_Folder, Data_Folder,Site_Hectares)
        
        # Repeat the process with the normalised solutions
        Extract_ParetoFront_and_Plot(Normalised_Gen, True, Each_Generations_Results_Folder, Data_Folder,Site_Hectares)
        Gen_count += 1