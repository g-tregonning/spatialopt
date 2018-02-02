# -*- coding: utf-8 -*-
"""
Module to evaluate spatial layout of development in London and return it's 
performance in several ojectives

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
data_folder= "C:/Users/danie_000/Python_Codes/Data/London/Rasters/100m Resolution/"

file_pointer = rasterIO.opengdalraster(data_folder+'Undev_new2.tif')  
Undev=rasterIO.readrasterband(file_pointer,1) 
driver, XSize, YSize, proj_wkt, geo_t_params = rasterIO.readrastermeta(file_pointer)
 
import numpy as np

def Plan(Developmen_Plan):
    # Function which takes an empty raster for the entire London Dataset and
    # assigns the development sites from the individual
    from copy import copy
    undev_copy = copy(Undev)
    # creating a blank array of london to add our new dwellings to
    Lndn_Dev_Plan =np.subtract(Undev,undev_copy)
    # looks up where each undeveloped site lies within the overall London plan
    import Undeveloped_Lookup # looks up where each
    # Currently ased on dwelling
    # multiply y average dsize dwelling if I want to change it
    for a in range(0,len(Developmen_Plan)):
        yx = Undeveloped_Lookup.Undev_Lookup[a]
        Lndn_Dev_Plan[yx]=Developmen_Plan[a]
    return Lndn_Dev_Plan        

def Calc_fheat(Developmen_Plan):
    # Import the heat hazard raster for the calculation
    Heat    = rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Heat.tif') ,1)
    # Need a vulneraility Raster!!!
    
    # Assign development Sites to Entire London
    Lndn_Dev_Plan = Plan(Developmen_Plan)
    
    # Need to incoprate Vulneraility
    # Do this by multiplying this array by average person per dwelling 
    # Add this to the a current Vulneraility array before multiplying by hazard     
        
    HeatRisk = np.multiply(Lndn_Dev_Plan, Heat)

    # Once vulnerability has een     
    
    return np.sum(HeatRisk)

def Calc_fflood(Developmen_Plan):
    # Floodzone Raster, 1 in 100 and 1 in 1000 floodzone represented by 100 and 1000 respectively     
    Floodzone   = rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Floodzone.tif'),1)
    
    import numpy as np   
    Lndn_Dev_Plan = Plan(Developmen_Plan)
    Floodzone_Reduced = np.divide(Floodzone, 100)
    FloodRisk = np.multiply(Lndn_Dev_Plan, Floodzone_Reduced)
    #print "Flood Risk is ", np.sum(FloodRisk)
    return np.sum(FloodRisk)
   
def Calc_fbrownfield(Developmen_Plan):
    # Calculate the number of proposed development sites which fall on 
    # brownfield sites. Target in London Plan is 96%, not enforcing this, 
    # will just use it as a comparison. Module works by multiplying the 
    # London wide plan by the brownfield dataset
    Brownfield      = rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'Brownfield.tif'),1)

    import numpy as np
    # So if they correlate with Brownfield 1x1 = 1 whilst if they dont either 
    # 0 x 1 or 1 x 0 = 0. Can then sum the array and the sum correlates with 
    # the numer of sites on Brownfield. In order to get a percentage (proBaBly
    # what I would return) I need a total amoutn of sites. Could achieve this 
    # counter then sum it. 
    
    Lndn_Development_Plan = Plan(Developmen_Plan)
    
    # Calculates a array Based on where Brnownfield sites correlate with 
    # development sites. If sites and brownfield don't correlate it becomes 
    # zero, else it remains a value. Then count the numBer of none zeros
    # to calculate number which are located on brownfield sites
    Brownfield_Correlates = np.count_nonzero(np.multiply(Brownfield,Lndn_Development_Plan))

    # Calculate the numBer of original sites in order to calculate a %
    Total_Sites     = np.count_nonzero(Developmen_Plan)
    # Convert the vairaBles to floats else we get a 0 as it does integer division
    Per_Brownfield  = (float(Brownfield_Correlates)/float(Total_Sites)) * 100  

    return Per_Brownfield
    #return 1

def Calc_fdensity(Developmen_Plan):
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
    
    # Compliance table [] denotes its acceptable
    # 		                    PTAL								
    #            2	3	4	5	6	7	8	9    10
    # De   60	[120	180	240	300	360	420	480	540	600]
    # ns	100	[200	300	400	500	600	700]	800	900	1000
    # ity 150	[300	450	600	750]	900	1050	1200	1350	1500
    #     350  [700	1050	1400	1750]2100	2450	2800	3150	3500

    # Import the Pulbic Transport Accessiility  in London Raster
    PTAL      = rasterIO.readrasterband(rasterIO.opengdalraster(data_folder+'PTAL.tif'),1)
    # Combine proposed development sites with wider London array
    Lndn_Development_Plan = Plan(Developmen_Plan)

    PTAL_Dev_Matrix = np.multiply(Lndn_Development_Plan, PTAL)
    
    from collections import Counter    
    PTAL_Dev_Count = Counter(PTAL_Dev_Matrix)
    
    # Calculate the number of times development sites don't meet the guidelines
    Sum_Fail = 0
    # List of all the possible results which indicate guideline hasnt been met    
    Fails_Guideline = [800,900,1000,1050,1200,1350,1500,2100,2450,2800,3150,3500]
    for fail in Fails_Guideline:
        # Add the count for each of these values
        Sum_Fail += PTAL_Dev_Count[fail]
    
    
    # Calculate the numBer of original sites in order to calculate a %
    Total_Sites     = np.count_nonzero(Developmen_Plan)
    Per_Fail = float(Sum_Fail)/float(Total_Sites)    
    Per_Success = 100 - Per_Fail
    return Per_Success

def Calc_fsprawl(Developmen_Plan):
    # Intend to do the non-linear neighourhood method again
    # Only prolem would be quite computationaly intensive
    
    return 1
    
def Calc_flocal(Developmen_Plan):
    # Intention to assess how well the proposed development and it's density
    # fits with the local neighourhood. This would require a spatial dataset 
    # on dwelling density. Possily get this from District Valuation Service 
    # Pretty sure it was at LSOA. Non-Linear Neighourhood method
    
    
    
    return 1