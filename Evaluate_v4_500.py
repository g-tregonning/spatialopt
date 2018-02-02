# -*- coding: utf-8 -*-
"""
Version 1_500
Module to evaluate spatial layout of development in London and return it's 
performance in several ojectives. 

Changes:
    + Using the newest edition of Undev_brwnfld_Inten
        # Airport remoed 
        # greenspace erased
        # intensification areas added
    + Upper development changed from 350 to 250
    + Working at 500m spatial resolution
    +   Changed the look up etc


Objectives currently optimised include:
    1. Heat Risk
        ~ Check the heat data
        ~ Is it too Big?
        
    2. Flood Risk
    
    3. Location of development on Brownfield sites
    
Need to consider weighting them based on the number of dwellings i.e. relative risk
    ~ Could scale it to what the total dwellings would be
"""
"""""""""""""""""""""""""""""""""""""""
# IMPORT DATASETS
"""""""""""""""""""""""""""""""""""""""
import rasterIO
data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/500m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undeveloped.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
 
import numpy as np

def Plan(Development_Plan):
    # Function which takes an empty raster for the entire London Dataset and
    # assigns the development sites from the individual
    from copy import copy
    undev_copy = copy(Undev)
    # creating a blank array of london to add our new dwellings to
    # tested the sum which is 0 
    # Making it a double so that the large values will be kept
    Lndn_Dev_Plan =np.double(np.subtract(Undev,undev_copy))
    

    # looks up where each undeveloped site lies within the overall London plan
    # Working at 500 metre spatial resoluton
    import Undev_brwnfld_Inten_Lookup_500 as Lookup
    # Currently ased on dwelling
    # multiply y average dsize dwelling if I want to change it
    # Getting problem that a lot of dwelling lost all of a sudden
    # Ok so problem is that 
    for a in range(0,len(Development_Plan)):
        yx = Lookup.Undev_Lookup[a]
            
        Lndn_Dev_Plan[yx]=Development_Plan[a]

    #print "non zeros of lndn dev plan", np.count_nonzero(Development_Plan) 
    
    #from collections import Counter  
    #print "Count Dev Plan", Counter(Development_Plan)
    #for x in Lndn_Dev_Plan:
     #   print x
   # print "after Planning", np.sum(Lndn_Dev_Plan)
    return Lndn_Dev_Plan        

def Calc_fheat(Development_Plan, Site_Size):
    # Import the heat hazard raster for the calculation
    # Making a double to handle large integers
    Heat    = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Heat.tif') ,1))
    # Need a vulneraility Raster!!!
    
    # Assign development Sites to Entire London and multiply by the site size
    Lndn_Dev_Plan = np.multiply(Plan(Development_Plan), Site_Size)
    
    # Need to incoprate Vulneraility
    # Do this by multiplying this array by average person per dwelling 
    # Add this to the a current Vulneraility array before multiplying by hazard     
        
    HeatRisk = np.multiply(Lndn_Dev_Plan, Heat)
    
    # Need to include the vulnerability metric at some point
    # Make this a per capita metric?
    # So divide by the total number of people?
    HeatRisk_per_Capita = np.sum(HeatRisk)/np.sum(Lndn_Dev_Plan)

    
    return HeatRisk_per_Capita

def Calc_fflood(Development_Plan, Site_Size):
    # Floodzone Raster, 1 in 100 and 1 in 1000 floodzone represented by 100 and 1000 respectively     
    import numpy as np    
    Floodzone   = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Floodzone.tif'),1))
    
       
    # Assign development Sites to Entire London and multiply by 25
    # As its at 500 m spatial resolution
    Lndn_Dev_Plan = np.multiply(Plan(Development_Plan), Site_Size)
    
    # Reduced as its currently at 1000 and 100. Could just change the dataset?
    # Change the dataset to 0.1 and 1? Should recongise 0.1 as old heat stuff
    # Was like that
    Floodzone_Reduced = np.divide(Floodzone, 100)
    FloodRisk = np.multiply(Lndn_Dev_Plan, Floodzone_Reduced)
    #print "Flood Risk is ", np.sum(FloodRisk)
    # Calculating a per capita metric as per heat in order to 
    FloodRisk_per_Capita = np.sum(FloodRisk)/np.sum(Lndn_Dev_Plan)
    return FloodRisk_per_Capita
   
def Calc_fbrownfield(Development_Plan):
    # Calculate the number of proposed development sites which fall on 
    # brownfield sites. Target in London Plan is 96%, not enforcing this, 
    # will just use it as a comparison. Module works by multiplying the 
    # London wide plan by the brownfield dataset
    # Currently works out the number of sites but could potentially
    # calculate the number of dwellings
    
    # NOTE!!!
    # Should this calculate the number of dwellings not on brownfield?
    # Justification would be allowing low density in outer london to not be
    # on brownfield. Need to use a sum instead if this is the case.     
    
    import numpy as np
    Brownfield      = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Brownfield.tif'),1))

    
    # So if they correlate with Brownfield 1x1 = 1 whilst if they dont either 
    # 0 x 1 or 1 x 0 = 0. Can then sum the array and the sum correlates with 
    # the numer of sites on Brownfield. In order to get a percentage (proBaBly
    # what I would return) I need a total amoutn of sites. Could achieve this 
    # counter then sum it. 
    
    Lndn_Development_Plan = Plan(Development_Plan)
    
    # Calculates a array Based on where Brnownfield sites correlate with 
    # development sites. If sites and brownfield don't correlate it becomes 
    # zero, else it remains a value. Then count the numBer of none zeros
    # to calculate number which are located on brownfield sites
    #Brownfield_Correlates = np.count_nonzero(np.multiply(Brownfield,Lndn_Development_Plan))
    
    # Calculting the number of dwellings which correspond as opposed to 
    Brownfield_Dwelling_Correlates = np.sum(np.multiply(Brownfield,Lndn_Development_Plan))


    # Calculate the numBer of original sites in order to calculate a %
    #Total_Sites     = np.count_nonzero(Development_Plan)
    # Calculate the number of dwellings in order to calc %
    Total_Dwells    = np.sum(Development_Plan)    
    
    # Convert the vairaBles to floats else we get a 0 as it does integer division
    #Per_Brownfield      = (float(Brownfield_Correlates)/float(Total_Sites)) * 100
    # In order for it to be a minimisation returns number of sites not located
    # on brownfield 
    #Per_Not_Brownfield  = (1-(float(Brownfield_Correlates)/float(Total_Sites)))* 100
    
    # Calculating this perentage based on the number of dwellings  
    Per_Not_Brownfield  = (1-(float(Brownfield_Dwelling_Correlates)/float(Total_Dwells)))* 100
    
    
    #return Per_Brownfield
    return Per_Not_Brownfield

def Calc_fdensity(Development_Plan):
    # Idea to see how well this complies with the density table (3.2) 
    # Assuming this is going to Be an oBjective function to optimise
    # Otherwise can just apply this function to the final solutions as a measure
    # A way to do this would be multiply, then we know what the products of
    # These should be ( 1 x 60, 2 x 60 etc) how often we get the right product.
    # Counter used to find them, i.e. counter[value] returns num
    # Prolem with this we could get the same values
    # Could also introduce a outer, inner and central london, and multiply it y this aswell
    # Need to decide on these prefered densities!!!
    # Target 95% to meet the guidelines
    # PTAL is Between 1 and 9. 
    # 1 = 6B, 2 = 6A .... Consider Changing this?
    # For example with 350 uph, I'd extract Counter[350] (PTAL 6a), Counter [700]
    # (PTAL 6B)...to Counter 1400 
    
    # Compliance table [] denotes its acceptable. Note PTAL goes from 2
    # as it allows for a better table
    # 		                    PTAL								
    #            2	3	4	5	6	7	8	9    10
    # De   60	[120	180	240	300	360	420	480	540	600]
    # ns	100	[200	300	400	500	600	700]	800	900	1000
    # ity 150	[300	450	600	750]	900	1050	1200	1350	1500
    #     250  [500	750	1000	1250]1500	1750	2000	2250	2500

    # Import the Pulbic Transport Accessiility  in London Raster
    # Importing it as a double so it can handle large integers
    PTAL      = np.double(rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'PTAL.tif'),1))
    # Combine proposed development sites with wider London array
    Lndn_Development_Plan = Plan(Development_Plan)
    
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

def Calc_fregeneration(Development_Plan):
    # Combine proposed development sites with wider London array
    Lndn_Development_Plan = Plan(Development_Plan)
    
    # Upload the regeneration areas raster
    Regeneration_Areas = rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Regeneration.tif'),1)

    # Multiply the lndn dev plan and regeneration areas
    # to extract how often they correspond
    Regenerated = np.multiply(Lndn_Development_Plan,Regeneration_Areas)
    
    # Count the number of times they correspond    
    Regen_Correlates = np.count_nonzero(Regenerated)
    
    # Calculate the numBer of original sites in order to calculate a %
    Total_Sites     = np.count_nonzero(Development_Plan)    
    
    Per_Not_Regen  = (1-(float(Regen_Correlates)/float(Total_Sites))) * 100  
    
    return Per_Not_Regen

def Calc_fsprawl(Development_Plan):
    # Intend to do the non-linear neighourhood method again
    # Only prolem would be quite computationaly intensive
    # Therefore I'm just going to multiply the two   
    
    # Combine the development plan with wider London array
    Lndn_Development_Plan = Plan(Development_Plan)
    
    Urban_Extent    = rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Urban.tif'),1)
    
    Total_Dev_Sites = np.count_nonzero(Lndn_Development_Plan)
    
    Sites_within_Urban_Extent = np.count_nonzero(np.multiply(Urban_Extent, Lndn_Development_Plan))
    
    Per_Not_within_Urban_Extent = (1-(float(Sites_within_Urban_Extent)/float(Total_Dev_Sites)))*100     
    
    return Per_Not_within_Urban_Extent
    
def Calc_flocal(Development_Plan):
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
    
        
    
    i,j = 0,0 # make this representative of the coordinates of development
    neighbour_density = 0 # variable to record the densities of the moore neighbhorhood
    # Investigate Moore Neighbourhood    
    for x in range(i-1,i+2):
        for y in range(j-1,j+2): 
             neighbour_density += Dwelling_Density[y,x]/5
    
    
    return 1
    

    
def Calc_ftravelcost(Development_Plan):
    # Intention to incorporate Ali's COST model

    return 1    
    
def Calc_fdist(Development_Plan):
    # Intention to calculate 
    
    return 1