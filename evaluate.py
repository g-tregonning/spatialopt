# -*- coding: utf-8 -*-
"""
Version 6

Latest version of Evaluation module.
Changes are that the the module recieves a London wide development plan

Objectives currently optimised include:
    1. Heat Risk (done per hhold)
        
    2. Flood Risk (returns per hhold)
    
    3. Location of development on Brownfield sites
    
    4. Sprawl
    
    5. Distance to CBD
    

"""

import rasterIO
import numpy as np
      

def Calc_fheat(London_Dwell_Plan, Heat):
    # Calculates a heat risk fitness based on hazard and vulnerability    
    
    
    # Import the heat hazard raster for the calculation
    # Making a double to handle large integers
    # Heat    = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(Data_Folder+'Heat_Hazard.tif') ,1))
    # Need a vulneraility Raster!!!
    
    # Need to incoprate Vulneraility
    # Do this by multiplying this array by average person per dwelling 
    # Add this to the a current Vulneraility array before multiplying by hazard     
        
    HeatRisk = np.multiply(London_Dwell_Plan, Heat)
    
    # Need to include the vulnerability metric at some point
    # Make this a per capita metric?
    # So divide by the total number of people?
    HeatRisk_per_Capita = np.sum(HeatRisk)/np.sum(London_Dwell_Plan)

    #print 'fheat ', HeatRisk_per_Capita 
    return HeatRisk_per_Capita

def Calc_fflood(London_Dwell_Plan, Floodzone):
    # Floodzone Raster, 1 in 100 and 1 in 1000 floodzone represented by 1 and 0.1 respectively
    # Recently realised that it should be the other way round as 1 in 1000 are actually at a lower risk 
    # of flooding     
    # Floodzone    = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(Data_Folder+'Floodzone.tif') ,1))


    FloodRisk = np.multiply(London_Dwell_Plan, Floodzone)
    #print "Flood Risk is ", np.sum(FloodRisk)
    # Calculating a per capita metric as per heat in order to 
    FloodRisk_per_Capita = np.sum(FloodRisk)/np.sum(London_Dwell_Plan)
    return FloodRisk_per_Capita
   
def Calc_fbrownfield(London_DwellPlan, Brownfield):
    # Calculate the number of proposed development sites which fall on 
    # brownfield sites. Target in London Plan is 96%, not enforcing this, 
    # will just use it as a comparison. 
    
    
    # Objectie function is calculated based on number of proposed sites 
    # which can be built on brownfield compared to total number of sites
    # Number of brownfield dwelings iis calculated based on the dev plan 
    # multiplied by the brownfield availability raster  
    
    # Brownfield = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(Data_Folder+'Brownfield.tif'),1))
    
    # Calculate the number of proposed sites
    Total_Dev_Sites = np.count_nonzero(London_DwellPlan)
    
    # Calculate the number of sites which occur on brownfield   
    Brownfield_Sites = np.count_nonzero(np.multiply(Brownfield, London_DwellPlan))
        
    # Calculating this perentage based on the number of dwellings  
    Per_Not_Brownfield  = (1-(float(Brownfield_Sites)/float(Total_Dev_Sites)))* 100
    
    
    #return Per_Brownfield
    return Per_Not_Brownfield
    
def Calc_fsprawl(London_Dwell_Plan, Urban_Extent):
    # Intend to do the non-linear neighourhood method again
    # Only prolem would be quite computationaly intensive
    # Therefore I'm just going to multiply the two   
    
    # Combine the development plan with wider London array
    
    # Urban_Extent    = rasterIO.readrasterband(rasterIO.opengdalraster(Data_Folder+'Urban.tif'),1)
    
    Total_Dev_Sites = np.count_nonzero(London_Dwell_Plan)
    
    # Calculate the number of sites within the urban extent
    Urban_Sites     = np.count_nonzero(np.multiply(Urban_Extent, London_Dwell_Plan))
    
    Per_Not_Urban   = (1-(float(Urban_Sites)/float(Total_Dev_Sites)))*100     
    
    return Per_Not_Urban   
    
def Calc_fgreenspace(London_Dwell_Plan, Greenspace):
    # Calculate the number of greenspace sites developed on

    # Greenspace       = rasterIO.readrasterband(rasterIO.opengdalraster(Data_Folder+'Greenspace.tif'),1)

    # Total_Dev_Sites  = np.count_nonzero(London_Dwell_Plan)
    
    Greenspace_Sites = np.count_nonzero(np.multiply(Greenspace, London_Dwell_Plan))  

    return Greenspace_Sites 
    
def Calc_fdist(Proposed_Sites, Greenspace_Development):
    # Function to calculate the average distance between proposed development
    # sites. Import a site lookup based on whether greenspace development is
    # allowed and lookup their shortest path distance to their closest CBD. This
    # value is added to a aggregate score and divided by the number of sites
    # Requires the 'Proposed Sites to be in ij format.
    
    if Greenspace_Development == True:
        import Dist_Lookup_GreenspaceDev as Dist_Lookup
    else:
        import Dist_Lookup as Dist_Lookup
    
        
    fdist_values = Dist_Lookup.fdist_lookup
    
    # Creating an aggregate of the shortest paths    
    agg_dist=0
    for dev_site in Proposed_Sites:
        # Quite an extensive 
        # Find its corresponding feature in the fdist lookup list
        # Need a quicker method of doing this        
        for site in fdist_values: 
            if dev_site==site[0]:
                # Add the shortest path to this site to an aggregate variable
                # Dividing by 1000 to convert to kilometres
                agg_dist+= site[1]/1000
    fdist = agg_dist/len(Proposed_Sites)

    return fdist
    
"""
def Calc_fdensity(Development_Plan, Spat_Res):
    # Idea to measure how well proposed development plans
    # complies with the London's plan density matrix (table 3.2) 
    # 
    # This is calculated by multiplying the PTAL array by the development plan
    # We then count the number of times certain values appear in the resulting 
    # raster. The values are shwon in the complaince table. [] denotes its 
    # meets the target. Note PTAL goes from 2 as it helped. 
    
    # 		                    PTAL								
    #            2	3	4	5	6	7	8	9    10
    #      35  [70  105  140  165  200  235  270  305  340]
    # De   60	[120	180	240	300	360	420	480	540	600]
    # ns	100	[200	300	400	500	600	700]	800	900	1000
    # ity 150	[300	450	600	750]	900	1050	1200	1350	1500
    #     250  [500	750	1000	1250]1500	1750	2000	2250	2500
    #     400  [800 1200 1600 2000]

    # Note PTAL raster value 2 represents PTAL 6b, whilst 9 represents 1b
    # 10 represents no data (ie its a greenspace area etc)
    data_spat_res_folder = data_folder+str(Spat_Res)+"m Resolution/"
    # Import the Pulbic Transport Accessiility  in London Raster
    # Importing it as a double so it can handle large integers
    PTAL      = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_spat_res_folder+'PTAL.tif'),1))
    # Combine proposed development sites with wider London array
    Lndn_Development_Plan = Plan(Development_Plan, Spat_Res)
    
    # Multiply the two arrays to distinguish how many times the guidelines are met
    PTAL_Dev_Matrix = np.multiply(Lndn_Development_Plan, PTAL)
    
    from collections import Counter
    # Convert the matrix into a 1D array using .ravel() in order to apply the Counter
    PTAL_Dev_Mat_1D =  PTAL_Dev_Matrix.ravel()
    PTAL_Dev_Count = Counter(PTAL_Dev_Mat_1D)
    #print PTAL_Dev_Count
    # Calculate the number of times development sites don't meet the guidelines
    Sum_Fail = 0
    # List of all the possible results which indicate guideline hasnt been met    
    Fails_Guideline = [800,900,1000,1050,1200,1350,1500,1750,2000,2250,2500]
    # Calculate the number of times the density guidelines aren't met
    for fail in Fails_Guideline:
        # Add the count for each of these values
        Sum_Fail += PTAL_Dev_Count[fail]
    
    # Calculate the numBer of original sites in order to calculate a %
    Total_Sites     = np.count_nonzero(Development_Plan)

    # In order for it Be a minimisation return the numBer of times the density
    # guidelines are not achieved
    Per_Fail        = float(Sum_Fail)/float(Total_Sites)*100  
    #print "Percentage Fails", Per_Fail
    #Per_Success     = (1 - Per_Fail)*100
    #return Per_Success
    return Per_Fail

def Calc_fregeneration(Development_Plan, Spat_Res):
    # Combine proposed development sites with wider London array
    Lndn_Development_Plan = Plan(Development_Plan, Spat_Res)
    
    data_spat_res_folder = data_folder+str(Spat_Res)+"m Resolution/"
    # Upload the regeneration areas raster
    Regeneration_Areas = rasterIO.readrasterband(rasterIO.opengdalraster(data_spat_res_folder+'Regeneration.tif'),1)

    # Multiply the lndn dev plan and regeneration areas
    # to extract how often they correspond
    Regenerated = np.multiply(Lndn_Development_Plan,Regeneration_Areas)
    
    # Count the number of times they correspond    
    Regen_Correlates = np.count_nonzero(Regenerated)
    
    # Calculate the numBer of original sites in order to calculate a %
    Total_Sites     = np.count_nonzero(Development_Plan)    
    
    Per_Not_Regen  = (1-(float(Regen_Correlates)/float(Total_Sites))) * 100  
    
    return Per_Not_Regen


    
def Calc_flocal(Development_Plan, Spat_Res):
    # Intention to assess how well the proposed development and it's density
    # fits with the local neighourhood. This would require a spatial dataset 
    # on dwelling density. Possily get this from District Valuation Service 
    # Pretty sure it was at LSOA. Non-Linear Neighourhood method
    
    # Considering the max and minimum local densities
    # 60 uha Min 0, Max 100
    # 100 uha Min 50, Max 150
    # 150 uha Min 100, Max 200
    # 350 uha Min 200, Max Infinite    
    
    # Algorithm would go:
    #   For each non-zero, D, in London Plan:
    #       Assess Moore neighbourhood = neighbourhood_density
    #       Max, Min = Density_limits(D)
    #       if neighbourhood_density > Max or < Min:
    #           locality penalty
    Dwelling_Density=[] # Load the dwelling density dataset    
    
    data_spat_res_folder = data_folder+str(Spat_Res)+"m Resolution/"        
    
    i,j = 0,0 # make this representative of the coordinates of development
    neighbour_density = 0 # variable to record the densities of the moore neighbhorhood
    # Investigate Moore Neighbourhood    
    for x in range(i-1,i+2):
        for y in range(j-1,j+2): 
             neighbour_density += Dwelling_Density[y,x]/5
    
    
    return 1

def Calc_fmixedlanduse(Development_Plan, Spat_Res):
    # Intention to provide a measure of the mixed landuse of London.
    # Currently the idea is to apply the non-linear neighbourhood method
    # to each proposed deelopment site and assess its neighbourhood for
    # econonmic landuse
    
    # Currently returns a 
    
    Economic_neighbour = 0    
    data_spat_res_folder = data_folder+str(Spat_Res)+"m Resolution/"    
    # imports the landuse raster. 1 is uncategorised, 2 represents economic
    # 3 represents residential. 
    Landuse     =  rasterIO.readrasterband(rasterIO.opengdalraster(data_spat_res_folder+'Landuse.tif'),1)

    # So going through the deelopment plan   
    for x in range(0,len(Development_Plan)):
        # Each site which has development proposed on it
        if Development_Plan[x] >0:
            # Import the lookup table to assess where it lies within the London 
            # development plan
            import London_Lookup as Lookup
    
            # Using the lookup module to generate a look up table    
            Undev_Lookup = Lookup.Generate_Lookup(Spat_Res)
            
            # Find the xy location of the site
            
            xy = Undev_Lookup[x]
            # split the xy location into x and y
            x = xy[1]
            y = xy[0]
            # assess the moore neighbourhood
            for i in range(x-1,x+2):
                for j in range(y-1,y+2): 
                    if Landuse[j,i]== 2: # 2 is value for economic landuse
                        Economic_neighbour +=1 
                        
    return Economic_neighbour
            

    
def Calc_ftravelcost(Development_PlanSpat_Res):
    # Intention to incorporate Ali's COST model

    return 1    
    
def Calc_fdist(Development_PlanSpat_Res):
    # Intention to calculate 
    
    return 1
    """