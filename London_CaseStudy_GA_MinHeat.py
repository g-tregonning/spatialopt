# -*- coding: utf-8 -*-
"""
Testing the use of newly developed method of itemising a development plan for 
London. Seeing if it'll work.
"""
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

"""""""""""""""""""""""""""""""""""""""
# DATASETS USED
"""""""""""""""""""""""""""""""""""""""
import rasterIO

data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/100m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undev_new2.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)

file_pointer = rasterIO.opengdalraster(data_folder+'Heat.tif')  
Heat=rasterIO.readrasterband(file_pointer,1) 

"""""""""""""""""""""""""""""""""""""""
#TYPES
#creating fitness class, negative weight implies minimisation 
"""""""""""""""""""""""""""""""""""""""
# Fitness
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Individual
creator.create("Individual", list, typecode='b', fitness=creator.FitnessMin)

"""""""""""""""""""""""""""""""""""""""
#INITIALIZATION
#Initially populating the types
"""""""""""""""""""""""""""""""""""""""
#Population
toolbox = base.Toolbox()


def Generate_Residential(Ind,Tot_Dwell):
    import random as rndm
    
    Density_Lookup = [0,60,100,150,350]
    agg, dev_list = 0,[]
    while agg < Tot_Dwell:
        dev = rndm.randint(1,4)
        agg +=  Density_Lookup[dev]
        dev_list.append(Density_Lookup[dev])
    
    Lndn_Plan = [0] * 19361
    for dev_site in dev_list:
        rand_site = rndm.randint(0,19361)
        if Lndn_Plan[rand_site]==0:
            Lndn_Plan[rand_site]=dev_site
            
    return Ind(Lndn_Plan)
    
Tot_Dwell = 340,000
toolbox.register("individual", Generate_Residential, creator.Individual, Tot_Dwell)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

"""""""""""""""""""""""""""""""""""""""
#OPERATORS
"""""""""""""""""""""""""""""""""""""""

def Eval_HeatRisk(Lndn_Plan):
    import numpy as np
    import copy    
    undev_copy = copy(Undev)
    

    New_Vuln =np.subtract(Undev,undev_copy)
    

    
    import Undeveloped_Lookup
    
    for a in range(0,len(Lndn_Plan)):
        yx = Undeveloped_Lookup.Undev_Lookup[a]
        New_Vuln[yx]=Lndn_Plan[a]
        
        
    Risk = np.multiply(New_Vuln, Heat)
    return np.sum(Risk),

toolbox.register("evaluate", Eval_HeatRisk)
# EVOLUTIONARY TOOLS

# Designate the method of crossover
toolbox.register("mate", tools.cxTwoPoints)
# Designate the method of mutation
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

"""""""""""""""""""""""""""""""""""""""
ALGORITHMS

"""""""""""""""""""""""""""""""""""""""

def GA():    
    # Genetic Algorithm    
    MU      = 50    # Number of individuals to select for the next generation
    NGEN    = 50     # Number of generations
    LAMBDA  = 100   # Number of children to produce at each generation
    CXPB    = 0.7   # Probability of mating two individuals
    MUTPB   = 0.2   # Probability of mutating an individual
    
    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    #stats.register("std", tools.std)
    stats.register("min", min)
    #stats.register("max", max)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN,stats= stats,
                              halloffame=hof)
    
    print "Length of HOF is ", len(hof)
                        
    return  hof
    
GA()