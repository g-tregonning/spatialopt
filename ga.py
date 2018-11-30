# -*- coding: utf-8 -*-
"""
Version 4 20/12/14

Genetic Algorithm to optimise the location of new residential development 
over the Greater London Authority. Genetic Algorithm facilitated by DEAP 
(Distributed Evolutionary Algorithms in Python) website: 
    (https://code.google.com/p/deap/)



Changes from previous versions:
    - Going to add in fdist
    - Attempting to work at a 100 metre spatial resolution
        + Too many issues with the availability raster
        + Although possibility in the future of coding it as [(uha, %),...]
    - Want to include an ability to develop on greenspace
        + Facilitated by a Greenspace_Development variable
            ~ Needs to change the fitness
            ~ Change the lookup
                + Need the ability to save a text file
            ~ 
        + 

Issues:
    - Issue being that if the density lookup is just 35s I dont think it can
        meet the dwell total
        + same with regards to 60,100 and 150 as they arent necessarily located 
    - Need to code initialisation so that it meets the PTAL objecties
        + Could this be an option for the User Interface
        + So enforcing a constraint
        + Would initialised
        + PTAL enforced initial variable



To do list:


The conversion to london devplan and london dwell plan isnt working
"""

"""""""""""""""""""""""""""
MODULES USED
Deap and RasterIO
"""""""""""""""""""""""""""
# DEAP modules to facilitate the genetic algorithm
from deap import algorithms
from deap import base 
from deap import creator # creates the initial individuals
from deap import tools # defines operators
import rasterIO

import numpy as np
import math
import random as rndm
from copy import copy

# Modules for the spatial optimisation framework
import initialise # initialisation module
import evaluate as Eval # Module to calculate and return fitnesses
import constraints as Constraint # Module handles the search constraints
import outputs as Output
from scenario import Scenario

import time

#from datetime import datetime
# from scoop import futures

 #log time for each module in GA
    # def log(event):
        # print('{} - {}'.format(event, datetime.now()))
start_time = time.asctime()
running_time_start = time.clock()

print "START. start time = ", start_time
print "Running time =", int(running_time_start), " minutes"

def start_run(scenario=Scenario()):
    def Generate_DevelopmentPlan(Ind, Tot_Dwell):

        Development_Plan = initialise.Generate_DevelopmentPlan(Tot_Dwell, scenario.dwelling_density,
                                                               No_Undev, lookup, scenario.site_area,
                                                               scenario.ptal_enforced, scenario.data_folder)
        # log('Created Development Plan')
        return Ind(Development_Plan)

    """""""""""""""""""""""""""""""""""""""
    # FUNCTIONS
    # Evaluate functions and constraint handling
    """""""""""""""""""""""""""""""""""""""

    def Evaluate(Development_Plan):
        # Generate the London Dwellings Plan i.e. number of dwellings on each site

        # London_DevPlan = Init.Generate_London_DevPlan(Development_Plan, Data_Folder)
        Proposed_Sites = initialise.Generate_London_Proposed_Sites(Development_Plan)

        London_DwellPlan = initialise.Generate_London_DwellPlan(Development_Plan, scenario.data_folder,
                                                                scenario.site_area)
        #log('Calculated Number of Dwellings')

        Heat_Fit = Eval.Calc_fheat(London_DwellPlan, scenario.data_folder)

        Flood_Fit = Eval.Calc_fflood(London_DwellPlan, scenario.data_folder)

        Dist_Fit = Eval.Calc_fdist(Proposed_Sites, scenario.greenspace_development)

        Brownfield_Fit = Eval.Calc_fbrownfield(London_DwellPlan, scenario.data_folder)

        Sprawl_Fit = Eval.Calc_fsprawl(London_DwellPlan, scenario.data_folder)

        if scenario.greenspace_development == True:
            Greenspace_Fit = Eval.Calc_fgreenspace(London_DwellPlan, scenario.data_folder)

            return Heat_Fit, Flood_Fit, Dist_Fit, Brownfield_Fit, Sprawl_Fit, Greenspace_Fit,

        else:
            return Heat_Fit, Flood_Fit, Dist_Fit, Brownfield_Fit, Sprawl_Fit

    def Track_Offspring():
        # Decrotor function to save the solutions within the generators
        def decCheckBounds(func):
            def wrapCheckBounds(*args, **kargs):
                offsprings = func(*args, **kargs)
                # Append this generations offspring
                Gens.append(offsprings)
                for child in offsprings:
                    # attach each individual solution to solution list
                    # Allows the demonstration of which solutions the Algorithm
                    # has investigated
                    Sols.append(child)
                return offsprings

            return wrapCheckBounds

        return decCheckBounds

    def Genetic_Algorithm():
        # Genetic Algorithm
        print "Beginning GA operation"

        # Create initialised population
        print "Initialising"
        pop = toolbox.population(n=MU)

        # hof records a pareto front during the genetic algorithm
        hof = tools.ParetoFront()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        # stats.register("avg", tools.mean)
        # stats.register("std", tools.std)
        stats.register("min", min)
        # stats.register("max", max)

        # Genetic algorithm with inputs
        algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN,
                                  stats=stats, halloffame=hof)

        return hof

    Problem_Parameters = ['Spatial Resolution (m^2)', scenario.resolution, 'Total Dwellings', scenario.total_dwellings,
                          'Minimum Dwellings', scenario.minimum_dwellings, 'Maximum Dwellings', scenario.maximum_dwellings,
                          'Site Hectares', scenario.site_area, 'Development Densities (uha)', scenario.dwelling_density,
                          'PTAL Constraint Enforced', scenario.ptal_enforced, 'Greenspace Developable',
                          scenario.greenspace_development, 'Greenspace Penalty', scenario.greenspace_penalty]



    Modules = ['Initialisation', initialise.__name__, 'Evaluation', Eval.__name__,
               'Constraint', Constraint.__name__, 'Output', Output.__name__]

    # To handle the constraints the algorithm uses a lookup for proposed development
    # sites. The lookup list contains the locations of sites available for development
    # and we optimise a series of numbers which correspond with these sites.
    # The function called creates a lookup based on our preferences, saves it and
    # returns the list.
    lookup = initialise.Generate_Lookup(scenario.greenspace_development, scenario.data_folder)
    No_Undev = len(lookup)
    # So we know how long to make the chromosome

    """""""""""""""""""""""""""
    PROBLEM FORMULATION
    # Variables for outputting
    """""""""""""""""""""""""""
    # For results
    Sols, Gens = [], []  # Saves all solutions found, saves each generation created

    # Keep a record of the retaintion after constraints
    start = []  # initial array
    # Resave the files to contain the arrays
    np.savetxt("PTAL_Constraint.txt", start, delimiter=',', newline='\n')
    np.savetxt("Dwell_Constraint.txt", start, delimiter=',', newline='\n')

    """""""""""""""""""""""""""""""""""""""
    #TYPES
    #creating fitness class, negative weight implies minimisation 
    """""""""""""""""""""""""""""""""""""""
    # FITNESS - Defining the number of fitness
    if scenario.greenspace_development == True:
        # fheat, fflood, fbrownfield, fgreenspace
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0, -1.0, (-1 * scenario.greenspace_penalty),))
    else:
        # fheat, fflood, fbrownfield
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0, -1.0,))

    # INDIVIDUAL
    creator.create("Individual", list, typecode='b', fitness=creator.FitnessMin)

    """""""""""""""""""""""""""
    #INITIALIZATION
    #Initially populating the types
    """""""""""""""""""""""""""
    toolbox = base.Toolbox()


    ######

    toolbox.register("individual", Generate_DevelopmentPlan, creator.Individual, scenario.total_dwellings)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    if scenario.greenspace_development == True:
        Fitnesses = ['fheat', 'fflood', 'fdist', 'fbrownfield', 'fsprawl', 'fgreenspacel']

    else:
        Fitnesses = ['fheat', 'fflood', 'fdist', 'fbrownfield', 'fsprawl']


    #######

    """""""""""""""""""""""""""""""""""""""
    OPERATORS
    Registers Operators and Constraint handlers for the GA
    """""""""""""""""""""""""""""""""""""""
    # Evaluator
    # Evaluation module- so takes the development plan
    # returns the oj functions
    # Evaluation =
    toolbox.register("evaluate", Evaluate)

    # EVOLUTIONARY OPERATORS

    # Designate the method of crossover
    # essentialy takes two points along the array and swaps the dwellings
    # Between them. Desingating the string name for the output text document
    Crossover = "tools.cxTwoPoint"
    # toolbox.register("mate", tools.cxTwoPoints)
    toolbox.register("mate", tools.cxTwoPoint)
    # Designate the method of mutation
    # Decided to use mutShuffleIndexes which merely moves the
    # elements of the array arround
    Mutation = "tools.mutShuffleIndexes, indpb=0.1"
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)

    # Selection operator. Either use this or SPEA2 as dealing with multiple OBjs
    # Could potentially write my own... don't think itd achieve much more.
    # See DeB, 2002 for details on NSGA2
    Selection = "tools.selNSGA2"
    toolbox.register("select", tools.selNSGA2)

    Operators = ['Selection', Selection, 'Crossover', Crossover, 'Mutation', Mutation]

    # CONSTRAINT HANDLING
    # Using a decorator function in order to enforce a constraint of the operation.
    # This handles the constrain on the total numBer of dwellings. So the module
    # interupts the selection phase and inestigates the solutions selected. If
    # they fail to exceed the minimum dwellings total or exceed the max dwellings
    # its deleted from the gene pool.
    # Moreoer to this, each generation is saed to the Gen_list and each generated
    # Solution is saved to a sol_list. This for display purposes.

    # Constraint to ensure the number of dwellings falls within the targets
    toolbox.decorate("select", Constraint.Check_TotDwellings_Constraint(scenario.minimum_dwellings, scenario.maximum_dwellings,
                                                                            scenario.data_folder, scenario.site_area))
    toolbox.decorate("select", Track_Offspring())
    # Constraint to handle PTAL enforcment
    if scenario.ptal_enforced == True:
        toolbox.decorate("select", Constraint.Check_PTAL_Constraint(scenario.data_folder))

    MU = 500  # Number of individuals to select for the next generation
    NGEN = scenario.number_of_iterations  # Number of generations
    # Think this will need to Be really high
    LAMBDA = 500  # Number of children to produce at each generation
    CXPB = 0.7  # Probability of mating two individuals
    MUTPB = 0.2  # Probability of mutating an individual

    GA_Parameters = ['Generations', NGEN, 'No of individuals to select', MU,
                     'No of children to produce', LAMBDA, 'Crossover Probability',
                     CXPB, 'Mutation Probability', MUTPB]

    # Returns the saved PO solution stored during the GA
    hof = Genetic_Algorithm()
    # log('Completed Genetic Algorithm')
    Complete_Solutions = copy(Sols)
    for PO in hof:
        Complete_Solutions.append(PO)

    # Update the results folder to the new directory specifically for this run
    Results_Folder = Output.New_Results_Folder(scenario.results_folder)

    # Format the solutions so they are compatible with the output functions
    # Gives each a number as well as added the fitness values to from:
    # [ Sol_Num, Sites, Fitnesses]
    frmt_Complete_Solutions = Output.Format_Solutions(Complete_Solutions)

    # Extract the minimum and maximum performances for each objective
    # To allow for solutions to be normalised
    MinMax_list = Output.Normalise_MinMax(frmt_Complete_Solutions)

    # Normalise the formatted Solution list using the Min and Maxs for
    # each objective function
    Normalised_Solutions = Output.Normalise_Solutions(MinMax_list, frmt_Complete_Solutions)


    # Output a file detailing all the run parameters
    Output.Output_Run_Details(Results_Folder, Modules, Operators, Problem_Parameters,
                              GA_Parameters, Fitnesses)

    # Extract all the Pareto fronts using the normalised solutions
    Output.Extract_ParetoFront_and_Plot(Normalised_Solutions, True, Results_Folder, scenario.data_folder, scenario.site_area)

    # Extract all the Pareto fronts using the solutions retaining their true values.
    Output.Extract_ParetoFront_and_Plot(frmt_Complete_Solutions, False, Results_Folder, scenario.data_folder, scenario.site_area)

    # GENERATIONS OUTPUTS

    # Create a new array to hold the formated generations
    frmt_Gens = []
    for Gen in Gens:
        # For each generation, format it and append it to the frmt_Gens list
        frmt_Gens.append(Output.Format_Solutions(Gen))

    #
    Output.Extract_Generation_Pareto_Fronts(frmt_Gens, MinMax_list, Results_Folder, scenario.data_folder, scenario.site_area)
    # log('Saved iteration results')

if __name__ == '__main__':

    start_run()