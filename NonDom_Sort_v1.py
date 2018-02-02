# -*- coding: utf-8 -*-
"""
Non dominated Sorting Algorithm to extract Pareto-optimal
between objectives. Recently rewritten to work with GA results
Results stored just as the values

Based on Mishra & Harit's Algorithm

needs solutions to be in format [obj1, obj2,...objn]

"""
from copy import copy 

def frmt(Sols):
    frmt_sols = []
    for sol in Sols:
        sol_objs = []
        # Now we are no longer working with just four
        # this takes the length of the fitness attribute
        for x in range(len(sol.fitness.values)):
            obj = sol.fitness.values[x] 
            sol_objs.append(obj)
        frmt_sols.append(sol_objs)
    
    return frmt_sols

def Sort(solutions, ObjFunc):
    # Mishra & Harit's Algorithm
    #print solutions
    
    NonDom_list = [] # list of non-dominated solutions to compare solutions to
    Solution_list = frmt(copy(solutions))    
    Solution_list.sort(key=lambda x: x[ObjFunc[0]], reverse = False) #currently sorted by smallest 1st obj    
    #print solutions
    NonDom_list.append(Solution_list[0]) #
    Solution_list.pop(0) 
    for Sol in Solution_list: #Check each solution in the solution list
        row_count = -1 #keep a track of which row of the non_dom_list incase it needs to be popped
        for NonDom_Sol in NonDom_list:
            row_count += 1
            #print Sol
            #print NonDom_Sol
            #ObjFunc
            Dominated, Dominates= Domination_Check(Sol,NonDom_Sol,ObjFunc)
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
        if Solution[ObjNum] < NonDom_Solution[ObjNum]: #changed to represent fitness values
            #print "found not to be dominated"
            Dominated = False
        if Solution[ObjNum] > NonDom_Solution[ObjNum]:
            #print "found not to dominate"            
            Dominates = False
    return Dominated, Dominates 