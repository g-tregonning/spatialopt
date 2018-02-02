# -*- coding: utf-8 -*-
"""
Exploring the idea of the London Case Study to be optimised on the basis of 
of a density as well as a proportion of the cell. Two options for this:
    1. Two grids:
        Density     [0,0,60,0,150...]
        Proportion  [0,0,0.2,0,0.6...]
    2. Contained within:
           Site, Proportion     
        [ (60, 0.4),...]
This version tests the second option
"""

from deap import algorithms
from deap import base 
from deap import creator # creates the initial individuals
from deap import tools # defines operators

import random as rndm

"""""""""""""""""""""""""""""""""""""""
#TYPES
#creating fitness class, negative weight implies minimisation 
"""""""""""""""""""""""""""""""""""""""
# FITNESS - Heat_Fit,Flood_Fit, Brownfield_Fit (positive oj func), Density_Fit   
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# INDIVIDUAL
creator.create("Individual", list, typecode='b', fitness=creator.FitnessMin)

Site_Min, Site_Max = 20, 100
Prop_Min, Prop_Max = 0, 10
No_Sites = 20

def Generate_DevelopmentPlan(ind, Site_Min, Site_Max, Prop_Min, Prop_Max, No_Sites):
    site_list = []    
    for n in range(0,No_Sites):
        Site = rndm.randint(Site_Min, Site_Max)
        Prop = rndm.randint(Prop_Min, Prop_Max)
        
        Site_Prop = (Site, Prop)
        site_list.append(Site_Prop)
    return ind(site_list)
        
    
    

toolbox = base.Toolbox()
toolbox.register("individual", Generate_DevelopmentPlan, creator.Individual,
                 Site_Min, Site_Max, Prop_Min, Prop_Max, No_Sites)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def Evaluate(Plan):
    # step through the plan in jumps of two
    sum = 0
    for i in range(0,len(Plan)):
        sum += (Plan[i][0] * (Plan[i][1]/10))
    
    return sum,
        
def Check():
    def decCheckBounds(func):
        def wrapCheckBounds(*args, **kargs):
            # Extract the offspring solutions
            offsprings = func(*args, **kargs)
            # Extract each of the children from the offspring
            for child in offsprings:
                # Appending all those found solutions
                for i in range(0,len(child)):
                    if child[i][1] > 10 or child[i][1] < 0:
                        print child[i]
                        print "ALERT!!!!"
                     
            #print offsprings
            return offsprings
        return wrapCheckBounds
    return decCheckBounds    

toolbox.register("evaluate", Evaluate)

# EVOLUTIONARY OPERATORS

toolbox.register("mate", tools.cxTwoPoints)

toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)

toolbox.register("select", tools.selRoulette)
toolbox.decorate("select", Check())

MU      = 50   # Number of individuals to select for the next generation
NGEN    = 10     # Number of generations
# Think this will need to Be really high
LAMBDA  = 50  # Number of children to produce at each generation
CXPB    = 0.7   # Probability of mating two individuals
MUTPB   = 0.2

def Genetic_Algorithm():    
    # Genetic Algorithm    
    print "Beginning GA operation"
    
    # Create initialised population  
    pop = toolbox.population(n=MU)
    
    # hof records a pareto front during the genetic algorithm
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("avg", tools.mean)
    #stats.register("std", tools.std)
    stats.register("min", min)
    #stats.register("max", max)
    
    # Genetic algorithm with inputs
    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN,
                              stats= stats, halloffame=hof)
             
    return  hof  

PO = Genetic_Algorithm()

for sol in PO:
    print sol