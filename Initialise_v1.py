# -*- coding: utf-8 -*-
"""
Initialise v1

Module for the initialisation. Takes the initial parameters from the GA module
and produces a DevelopmentPlan ([0,0,60,400,... etc]). Within this module we'd
also include all the settings such as ensuring it's within brownfield and 
all high density

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
        @ Based on the paramters given the function creates a 
"""
import random as rndm
import numpy as np
import rasterIO


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

    return Lookup

                               
def Generate(Tot_Dwell, No_Undev,Availability_Raster,
                             Density_Lookup, PTAL,Undev_Lookup, Site_Hectares,
                             PTAL_Enforced):
    # Intention to assign densities from the density lookup to a London 
    # array. Number of dwellings assigned is decided by the per undeveloped land
    # density per hectare multplied by the percentage of undeveloped which is
    # multiplied by the Site_Hectares
    # Assign development densities to this array which is the length of the 
    # lookup array
    Development_Plan    = [0]*3572
    Dwellings_Plan      = [0]*3572     
    # Assign the number of development proposed to this array (for the purposes of
    # calculating risk etc)
    Dwellings_Plan = np.double(np.copy(Development_Plan))    
    
    # Store the aggregate number of dwelling assigned by the proposed development plan 
    Agg_Dwell = 0
    
    # Import the ptal dataset to 
    file_pointer = rasterIO.opengdalraster(Data_Folder+'ptal.tif') 
    PTAL = rasterIO.readrasterband(file_pointer,1)     
    
    
    while Agg_Dwell < Tot_Dwell:
        
        # Select a random site which isn't fully developed
        x = rndm.randint(0,No_Undev-1)
        
        # Selects a random density
        rand = rndm.randint(0,len(Density_Lookup)-1)
        Dev_Density = Density_Lookup[rand]        
        
        # If there isnt 0% space available from development
        # Check development hasn't alread been designated there
        if Development_Plan[x] == 0 and Availability_Raster[Undev_Lookup[x]]!= 0:

            import Constaints_v1 as Constraint
            if PTAL_Enforced == True and Constraint.PTAL_Constraint(PTAL, Undev_Lookup[x], Dev_Density) == True  or PTAL_Enforced == False:
                # assign the prescribed development density to the site             
                Development_Plan[x] = Dev_Density

                # assign the prescribed number of dwellings based on the density per
                # hectare, the percentage land available and the area of each site
                Availabile_Land     = (Availability_Raster[Undev_Lookup[x]]*Site_Hectares)/100
                
                Dwellings_Plan[x]   = Availabile_Land * Dev_Density 
                Agg_Dwell = np.sum(Dwellings_Plan)
             
    return Development_Plan


def Generate_DevelopmentPlan(Tot_Dwell, Density_Lookup, No_Undev, Lookup, 
                             Site_Hectares, PTAL_Enforced, Data_Folder):
        
        # Function allows for the setting of parameters when generating a spatial
        # plan. To enhance the initialisation the algorithm skews some of the
        # initial plans to represent extremes. This combined with completely
        # random plans allows for a better Pareto front. 
        
        # 
        Density_Prob    = rndm.randrange(4,6) 
        Brownfield_Prob = rndm.random()

        if rndm.random()<0.3:
            Density_Lookup = [Density_Lookup[Density_Prob]]#*len(Density_Lookup)
        



        # so the problem Im having is that a dev plan which meets the dwell 
        # targets just on brownfield then has too much when projected on to the 
        # availability raster
        if Brownfield_Prob > 1:
        # Dont think this will work as assigning densities to brwnfield areas
        # so later on when actually assigning the densities there will be much
        # more houses
            # Replace the lookup table
            #import Brownfield_Lookup as Lookup
            #Undev_Lookup = Lookup.Brownfield_Lookup
            
            #No_Undev = len(Undev_Lookup)
            
            import rasterIO
            file_pointer = rasterIO.opengdalraster(Data_Folder+'Brownfield.tif')  
            Availability_Raster=rasterIO.readrasterband(file_pointer,1) 
               


        Development_Plan = Generate(Tot_Dwell, No_Undev,Availability_Raster,
                             Density_Lookup, Lookup, Site_Hectares,
                             PTAL_Enforced)                          
                                 
                                 
        return Development_Plan                           



    
def  Generate_London_DevPlan(Development_Plan, London_Array, Lookup, Boundary):
     # Produce London wide Dev plan
 
     # Create an empty raster with the dimensions of London
     London_DevPlan      = np.double(np.copy(London_Array))

    # for eachsite in the Development Plan (with the same length as the lookup)
     #print "len lookup ", len(Lookup)
     #print "len plan ", len(Development_Plan)
     for x in range(0, len(Lookup)-1):
         
         # find the sites yx location over London
         yx =  Lookup[x]
         # Add the proposed development to the London wide development plan
         #print London_DevPlan[yx] 
         #print Development_Plan[x]
         London_DevPlan[yx] = Development_Plan[x]
     #multiplying it to try stop it being square in the raster
     return np.multiply(London_DevPlan,Boundary)

def Generate_London_DwellPlan(Development_Plan, London_Array, Lookup, Availability_Raster,Boundary):
    London_DevPlan = Generate_London_DevPlan(Development_Plan, London_Array,
                                                         Lookup, Boundary)
    # multiplyng by 0.25 is 25 hectares divided by 100 because the percentage 
    # available is btwn 100
    London_DwellPlan = np.multiply(0.25,np.multiply(Availability_Raster, 
                                                    London_DevPlan))
                                                
    return London_DwellPlan
