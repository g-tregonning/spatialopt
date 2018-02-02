# -*- coding: utf-8 -*-
"""
Initialise v3

Module for the initialisation. Takes the initial parameters from the GA module
and produces a DevelopmentPlan ([0,0,60,400,... etc]). Within this module we'd
also include all the settings such as ensuring it's within brownfield and 
all high density. Added a while loop to stop the code hanging when the parameters
for a development plan dont meet the total dwellings.

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
        @ Had trouble with the code hanging so have some code to catch it
            + If the code repeats for over 100,000 times without the Agg_Dwell 
                changing
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
        @ It then calls the 'Generate' function
        @ This is entirely contained within a while loop which ensures the code doesnt hang
            # If the paramters chosen can't meet the total dwellings it returns false
            # And continues until a check != False, at which point it breaks
"""
import random as rndm
import numpy as np
import rasterIO
from copy import copy

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
    
    # Handles preventing the code hanging
    check_sum   = 0 # stores the previous Agg_Dwell to indicate if its changed
    check_count = 0 # counts the number of iterations the Agg_Dwell remains unchanged

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
        
        # Prevents the code hanging
        if check_sum == Agg_Dwell:
            # if the Agg_Dwell was the same on the last iteration the count is
            # increased
            check_count += 1
        else:
            # if Agg_Dwell is different reset count and take the new Agg_Dwell 
            check_count = 0
            check_sum = Agg_Dwell
            
        # If the iteration has gone through with no change return false   
        if check_count > 100000:
            #print "Caught hanging"           
            return False    
            
            
    return Development_Plan


def Generate_DevelopmentPlan(Tot_Dwell, Density_Lookup, No_Undev, Lookup, 
                             Site_Hectares, PTAL_Enforced, Data_Folder):
        
        # Function allows for the setting of parameters when generating a spatial
        # plan. To enhance the initialisation the algorithm skews some of the
        # initial plans to represent extremes. This combined with completely
        # random plans allows for a better Pareto front. 
        
        # To handle the while loop
        Orig_Density_Lookup = Density_Lookup        
        
        # Probabilites of skewing the development plan
        Density_Prob    = 0.5 # probability of altering the density lookup 
        Brownfield_Prob = 0.5 # probability of skewing development to brownfield
        Cluster_Prob    = 0.5 # probability of clustering development
         
        # Using a while loop to stop the code hanging with inputs that won't 
        # reach the prescribed dwell total. If Generate() doesn't return false
        # the while loop breaks and returns the development plan
        while True:
            Density_Lookup = Orig_Density_Lookup
            if Density_Prob > rndm.random():
                
                # CHECK theres sufficient dwellings being created
                No_of_Densities = rndm.randint(1, len(Density_Lookup))            
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
                # CHECK need to consider RuntimeWarning: overflow encountered in multiplyif this allows for a development to be 
                # built
                
                # select random proportion btwn 0 - 0.7 for site min
                Rndm_Prp = rndm.randint(0, 7)/10           
                
                Site_Min = Site_Max * (Rndm_Prp)
                
                # then select Site_Max based on increase of 0.3 from the Site_Min    
                Site_Max = Site_Max * (Rndm_Prp + 0.3)
                #print Density_Lookup
                
                # Attempt to generate a plan with these inputs
            Development_Plan = Generate(Tot_Dwell, No_Undev,Availability_Raster,
                                     Density_Lookup, Site_Hectares, Site_Min, Site_Max,
                                     PTAL_Enforced, Data_Folder)    
                                     
            if Development_Plan != False:
                # if Generate returns an array and not false break from the 
                # while loop
                break
            #print Development_Plan 
                
        return Development_Plan                           

def Generate_London_Proposed_Sites(Development_Plan):
     Lookup = (np.loadtxt("lookup.txt",delimiter=",")).tolist()
     
     Proposed_Sites_List = []
     # for eachsite in the Development Plan (with the same length as the lookup)
     for j in range(0, len(Lookup)-1):
         if Development_Plan[j] > 1:
             # find the sites yx location over London
             ji =  tuple(Lookup[j])
             Proposed_Sites_List.append(ji)
             
     return Proposed_Sites_List
         
def Generate_London_DevPlan(Development_Plan, Data_Folder):
     # Produce London wide development plan with 
     
     file_pointer        = rasterIO.opengdalraster(Data_Folder+'Empty_DevPlan.tif')  
     London_DevPlan      = np.double(np.copy(rasterIO.readrasterband(file_pointer,1)))
     
     file_pointer        = rasterIO.opengdalraster(Data_Folder+'Boundary.tif')     
     Boundary            = np.double(np.copy(rasterIO.readrasterband(file_pointer,1)))
     
     # Upload the lookup table from the generated file.
     Lookup = (np.loadtxt("lookup.txt",delimiter=",")).tolist()
     
     # for eachsite in the Development Plan (with the same length as the lookup)
     for j in range(0, len(Lookup)-1):
         
         # find the sites yx location over London
         ji =  tuple(Lookup[j])
         
         # Add the proposed development to the London wide development plan
         #print Development_Plan[j]
         London_DevPlan[ji] = Development_Plan[j]
         
     # multiplying it to try stop it being square in the raster
     return np.multiply(London_DevPlan,Boundary)

def Generate_London_DwellPlan(Development_Plan, Data_Folder, Site_Hectares):
    London_DevPlan = Generate_London_DevPlan(Development_Plan, Data_Folder)
    
    # Because we arent using an % available
    London_DwellPlan = np.multiply(London_DevPlan, Site_Hectares)
   
    return London_DwellPlan

"""
    old code from when we were using the availability aspect                                          
    file_pointer        = rasterIO.opengdalraster(Data_Folder+'Available.tif')  
    Availability_Raster = rasterIO.readrasterband(file_pointer,1)
                                                       
    London_DwellPlan = np.multiply(np.multiply(Availability_Raster, London_DevPlan), Site_Hectares)
                                                
    return London_DwellPlan
"""