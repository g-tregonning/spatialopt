# -*- coding: utf-8 -*-
"""
NON DOMINATED SORTING ALGORITHM TO EXTRACT PARETO-OPTIMAL
FOR RISK AND SUSTAINABILITY OBJECITVES USING AN ALGORITHM
BASED ON MISHR AND HARIT'S ALGORITHM
"""
Obj_Col = 2 #specifies that obj funcs are stored in 3rd column
HeatRisk_Fit, FloodRisk_Fit, Dist_Fit, Sprawl_Fit = 0,1,2,3
from copy import copy 
def NonDom_Sort(Solutions):
    print "Begining Non-Dominated Sorting Procedure"
    Pareto_Heat_Flood_Dist_Sprawl = Sort(Solutions, [HeatRisk_Fit, FloodRisk_Fit, Dist_Fit, Sprawl_Fit])    
    Pareto_Heat_Flood = Sort(Solutions, [HeatRisk_Fit, FloodRisk_Fit])
    Pareto_Heat_Dist = Sort(Solutions, [HeatRisk_Fit, Dist_Fit])
    Pareto_Heat_Sprawl = Sort(Solutions, [HeatRisk_Fit, Sprawl_Fit])
    Pareto_Flood_Dist = Sort(Solutions, [FloodRisk_Fit, Dist_Fit])
    Pareto_Flood_Sprawl = Sort(Solutions, [FloodRisk_Fit,Sprawl_Fit])
    Pareto_Sprawl_Dist = Sort(Solutions, [Dist_Fit, Sprawl_Fit])
    
    return Pareto_Heat_Flood_Dist_Sprawl, Pareto_Heat_Flood, Pareto_Heat_Dist, Pareto_Heat_Sprawl, Pareto_Flood_Dist, Pareto_Flood_Sprawl, Pareto_Sprawl_Dist

def Sort(solutions, ObjFunc):
    # Mishra & Harit's Algorithm
    #print solutions
    NonDom_list = [] # list of non-dominated solutions to compare solutions to
    Solution_list = copy(solutions)    
    Solution_list.sort(key=lambda x: x[Obj_Col][ObjFunc[0]], reverse = False) #currently sorted by smallest 1st obj    
    #print solutions
    NonDom_list.append(Solution_list[0]) #
    Solution_list.pop(0) 
    for Sol in Solution_list: #Check each solution in the solution list
        #print "Sol", Sol        
        row_count = -1 #keep a track of which row of the non_dom_list incase it needs to be popped
        for NonDom_Sol in NonDom_list:
            row_count += 1
            Dominated, Dominates= Domination_Check(Sol[Obj_Col],NonDom_Sol[Obj_Col],ObjFunc)
            if Dominated == True:
                #print "Solution ", Sol[0], " is Dominated by solution ", NonDom_Sol[0]
                break
            elif Dominates == True:
                #print "Solution ", Sol[0], " Dominates ", NonDom_Sol[0], " which is popped"
                NonDom_list.pop(row_count)
                break
        if Dominated == False:
            #print "Attaching ",Sol[0], " to the Non dominated list "
            NonDom_list.append(Sol)            
    return NonDom_list
         
def Domination_Check(Solution, NonDom_Solution,ObjFunc):
    Dominates = True # Stores if the solution dominates any solutions in the non dom list
    Dominated = True # Stores if the solution is dominated by a solution in the non dom list  
    for ObjNum in (ObjFunc):
        #print "Assessing ",  Solution[ObjNum], " and ", NonDom_Solution[ObjNum]
        if Solution[ObjNum] < NonDom_Solution[ObjNum]:
            #print "found not to be dominated"
            Dominated = False
        if Solution[ObjNum] > NonDom_Solution[ObjNum]:
            #print "found not to dominate"            
            Dominates = False
    return Dominated, Dominates

