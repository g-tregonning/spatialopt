# -*- coding: utf-8 -*-
"""
Initialise v1

Module for the initialisation. Takes the initial parameters from the GA module
and produces a DevelopmentPlan ([0,0,60,400,... etc]). Within this module we'd
also include all the settings such as ensuring it's within brownfield and 
all high density.

Changes:
    + Ignoring the % devleopable
    + Instead going for a high spatial resolution

Notes:
    + PTAL enforced during the initialisation
        - So going to use a PTAL enforced boolean to 
        - 96% compliance, therefore a 0.04 chance of it slipping through?
                @ if random =< 0.04

Functions:
    + Generate_Lookup
        @ Depending on paramters it opens a specific availability raster
        @ Then by running through it, identifies sites which are developable
        @ These are saved to a lookup list, which is saved as txt and returned
    + Generate
        @ Based on the paramters given the function creates a development plan
        @ As well as a dwelling plan (for the number of dwellings)
        @ This is done as a loop repeating through until the number of dwellings
            meets the total needed
    + Generate_DevelopmentPlan
        @ This function allows for the skewing of development to the extremes
        @ This provides a much better initialisation leading to better results
        @ Three things are changed based on probabilities:
            1 Density
                - Density is skewed so only a select set of densities are used
                - this is facilitated by random.sample
            2 Brownfield
                - Ensures development is exclusively located on brownfield sites
                - This is done by replacing the availability raster with the
                    brownfield raster
            3 Cluster
                - Limits the range in which development can be situated
                - This way we will get clustering of development
                - Need to check this doesnt cause problems 
        @ It then call
"""
import random as rndm
import numpy as np
import rasterIO
from copy import copy

Data_Folder     = "C:/Users/danie_000/Python_Codes/Data/London/"

file_pointer        = rasterIO.opengdalraster(Data_Folder+'Boundary.tif')  
Boundary_Raster     = rasterIO.readrasterband(file_pointer,1)
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)

Bound_copy = copy(Boundary_Raster)
Empty_Raster = np.subtract(Bound_copy, Bound_copy)

def Generate_Lookup(Greenspace_Development, Data_Folder):
    # If greenspace development is permissable a alternate availability raster
    # is selected.    
    if Greenspace_Development == True:
        File = "Available_Greenspace.tif"
    else: 
        # file is the basic availabilty raster
        File = "Available.tif"
    
    # Import the Availability Raster to identify sites for the lookup
    file_pointer        = rasterIO.opengdalraster(Data_Folder+File)  
    Availability_Raster = rasterIO.readrasterband(file_pointer,1) 
    driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
    
    Lookup = [] # Array to hold the location of available sites   
    
    # Investigate for all x and y combinations in the file
    for x in range(0,XSize):
        for y in range(0,YSize):
            # If the yx location yeilds a available site
            if Availability_Raster[y,x]==1:
                # format it and append it to the lookup list
                yx = (y,x)
                Lookup.append(yx)
    
    # save to a txt file so other modules can load it
    np.savetxt("lookup.txt", Lookup,  delimiter=',', newline='\n')       

    # return the lookup list
    return Lookup

                               
def Generate(Tot_Dwell, No_Undev, Availability_Raster, Density_Lookup, 
             Site_Hectares, Site_Min, Site_Max, PTAL_Enforced, Data_Folder):
    # Function creates a Development_Plan based on the density lookup, 
    # PTAL enforcement,  Availability_Raster, Site_Min and Site_Max
    # Density
    
    # NOTE: Could do with a time out exception

    # Assign development densities to this array which is the length of the 
    # lookup array
    Development_Plan    = [0]*No_Undev # Stores proposed development densities
    Dwellings_Plan      = [0]*No_Undev # Stores the     
    Agg_Dwell           = 0 #Aggregate number of dwellings assigned 
    
    # Upload the lookup table from the generated file.
    Lookup = (np.loadtxt("lookup.txt",delimiter=",")).tolist()
    
    # Import the ptal dataset for the constraint 
    file_pointer = rasterIO.opengdalraster(Data_Folder+'ptal.tif') 
    PTAL = rasterIO.readrasterband(file_pointer,1)     
    
    # Ensure enough dwellings are assigned
    while Agg_Dwell < Tot_Dwell:
        # Select a random site which isn't fully developed
        j   = rndm.randint(0,No_Undev-1)
        
        # Selects a random development density
        rand = rndm.randint(0,len(Density_Lookup)-1)
        Dev_Density = Density_Lookup[rand] 
        
        # Extract the ji location of the site
        ji  = tuple(Lookup[j])   
        

        # Check development hasn't alread been designated there and that it is
        # available for development (latter needed because of brownfield skewing)
        if Development_Plan[j] == 0 and Availability_Raster[ji]!= 0:
            # Enforce the PTAL constraint that low development density cannot
            # take place in highly accessibilty areas
            import Constaints_v1 as Constraint
            if PTAL_Enforced == True and Constraint.PTAL_Constraint(PTAL, ji, Dev_Density) == True  or PTAL_Enforced == False:
                # assign the prescribed development density to the site             
                Development_Plan[j] = Dev_Density

                # assign the prescribed number of dwellings based on the density per
                # hectare and the area of each site
                Dwellings_Plan[j]   = Site_Hectares * Dev_Density 
                Agg_Dwell = np.sum(Dwellings_Plan)
             
    return Development_Plan


def Generate_DevelopmentPlan(Tot_Dwell, Density_Lookup, No_Undev, Lookup, 
                             Site_Hectares, PTAL_Enforced, Data_Folder):
        
        # Function allows for the setting of parameters when generating a spatial
        # plan. To enhance the initialisation the algorithm skews some of the
        # initial plans to represent extremes. This combined with completely
        # random plans allows for a better Pareto front. 
        
        # Probabilites of skewing the development plan
        Density_Prob    = 0.2 # probability of altering the density lookup 
        Brownfield_Prob = 0.0 # probability of skewing development to brownfield
        Cluster_Prob    = 0.0 # probability of clustering development
                
        
        if Density_Prob > rndm.random():
            # CHECK theres sufficient dwellings being created
            No_of_Densities = rndm.randint(3, len(Density_Lookup))            
            Density_Lookup  = rndm.sample((Density_Lookup), No_of_Densities)
        
        if Brownfield_Prob > rndm.random():
            # Changes the availabilty raster to the brownfield one to skew 
            # development to brownfield sites
            file_pointer        = rasterIO.opengdalraster(Data_Folder+'Brownfield.tif')  
            Brownfield_Raster   = rasterIO.readrasterband(file_pointer,1) 
            Availability_Raster = Brownfield_Raster 
        else: 
            file_pointer        = rasterIO.opengdalraster(Data_Folder+'Available.tif')  
            Availability_Raster = rasterIO.readrasterband(file_pointer,1)  
            
        # Sites randomly picked from this range
        Site_Min, Site_Max = 0, No_Undev
        
        if Cluster_Prob > rndm.random():
            # reduces the range of sites which can be utilised to result in 
            # clusters of development
            # CHECK need to consider if this allows for a development to be 
            # built
            
            # select random proportion btwn 0 - 0.7 for site min
            Rndm_Prp = rndm.randint(0, 7)/10           
            
            Site_Min = Site_Max * (Rndm_Prp)
            
            # then select Site_Max based on increase of 0.3 from the Site_Min    
            Site_Max = Site_Max * (Rndm_Prp + 0.3)
        print Density_Lookup
        Development_Plan = Generate(Tot_Dwell, No_Undev,Availability_Raster,
                             Density_Lookup, Site_Hectares, Site_Min, Site_Max,
                             PTAL_Enforced, Data_Folder)                          
                                                                  
        return Development_Plan                           


def  Generate_London_DevPlan(Development_Plan, Data_Folder):
     # Produce London wide development plan with 
     
     file_pointer        = rasterIO.opengdalraster(Data_Folder+'Boundary.tif')  
     Boundary_Raster     = rasterIO.readrasterband(file_pointer,1)

     # Create an empty raster with the dimensions of London     
     #file_pointer        = rasterIO.opengdalraster(Data_Folder+'Empty_London_Raster.tif')  
     #London_DevPlan      = rasterIO.readrasterband(file_pointer,1)
     London_DevPlan      = np.double(np.copy(Empty_Raster))
     
     # Upload the lookup table from the generated file.
     Lookup = (np.loadtxt("lookup.txt",delimiter=",")).tolist()
     
     # for eachsite in the Development Plan (with the same length as the lookup)
     for j in range(0, len(Lookup)-1):
         
         # find the sites yx location over London
         ji =  tuple(Lookup[j])
         
         # Add the proposed development to the London wide development plan
         London_DevPlan[ji] = Development_Plan[j]
         
     # multiplying it to try stop it being square in the raster
     return np.multiply(London_DevPlan,Boundary_Raster)

def Generate_London_DwellPlan(Development_Plan, Data_Folder, Site_Hectares):
    London_DevPlan = Generate_London_DevPlan(Development_Plan, Data_Folder)
                                                         
    file_pointer        = rasterIO.opengdalraster(Data_Folder+'Available.tif')  
    Availability_Raster = rasterIO.readrasterband(file_pointer,1)
                                                       
    London_DwellPlan = np.multiply(np.multiply(Availability_Raster, London_DevPlan), Site_Hectares)
                                                
    return London_DwellPlan
