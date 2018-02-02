# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 20:01:00 2014
Calculate_fdist_values

Module intends to calculate the distances from all possible sites within the 
study area producing a lookup table (fdist_lookup). Unfortunatly NetworkX greatly increases
the running time, therefore instead of calculating a performance in fdist each
iteration of the optimisation, we instead refer the development sites to this
lookup table (fdist_lookup)

"""

import networkx as nx
import rasterIO
import numpy as np

data_folder = "C:/Users/a8093548/PhD/Python_Codes/Data/London/"

# Road network which forms the path
Road_Network    = nx.read_shp(data_folder+'Road_Network.shp')
# The CBD point file which we are calculating the shortest path distance to
CBD_Nodes       = nx.read_shp(data_folder+'Town_Centres.shp')

# Extracting the dataset for potential sites to calculate fdist from each one
file_pointer    = rasterIO.opengdalraster(data_folder+'Available.tif')    
Available       = rasterIO.readrasterband(file_pointer,1)

# Extracting the geotrans which is necessary for caluclating the centroids
# of potential development sites
d,X,Y,p,geotrans= rasterIO.readrastermeta(file_pointer)

def Generate_Development_Sites(Available_Sites):
    # Calculates a list of all the sites which we want to calculate the 
    # shortest pathfdist_values_Available.csv to. 
    Sites_to_Calc = []
    for x in range(0,X):
        for y in range(0,Y):
            siteyx = (y,x)
            if Available_Sites[siteyx] == 1:
                Sites_to_Calc.append(siteyx)
    

                
    return Sites_to_Calc

def Conv_2_Coords(list_of_sites, geo_t_params):
    # Calculates the geographical reference point of a centroid for each 
    # possible development site
    # Inputs are y,x
    # NOTE: Need to somehow check the y and x are the right way round
    count= 0   #
    array = []
    site_nodes = []
    for site in list_of_sites:
        y = site[0]
        x = site[1]
        # coord = coord of raster corner + (cell_coord * cell_size) + (cell_size/2)
        x_coord = geo_t_params[0] + (x*geo_t_params[1]) + (geo_t_params[1]/2)
        y_coord = geo_t_params[3] - (y*geo_t_params[1]) + (geo_t_params[5]/2)
        #print y_coord, x_coord
        
        # Have to work in x and y I think
        node_coord=(x_coord, y_coord)
        
        site_nodes.append(node_coord)    
        
        a = [count, x_coord, y_coord, x, y]
        array.append(a)
        count += 1 
                
    
    np.savetxt('C:/Users/a8093548/PhD/Available_Sites.csv', array, delimiter = ',')
          
        
    print "saved"
    return site_nodes
    
def calc_closest(new_node, node_list):
    best_diff = 10000
    closest_node=[0,0]
    for comp_node in node_list.nodes():
        
        diff = (abs(comp_node[0]-new_node[0])+abs(comp_node[1]-new_node[1]))
        if abs(diff) < best_diff:
            best_diff = diff
            closest_node = comp_node
            
    return closest_node
    
def Add_CBD_Nodes_To_Network(node_list,network):
    # Adds an edge between the node and the node calculated to be closest    
    for node in node_list:
        # Calculate the closest road node
        closest_node= calc_closest(node, network)
        network.add_node(node) #adds node to network
        network.add_edge(node,closest_node) #adds edge between nodes
        
def Add_Nodes_To_Network(node_list,network):
    # Adds an edge between the node and the node calculated to be closest    
    for node in node_list:
        # Calculate the closest road node
        closest_node= calc_closest(node, network)
        
        network.add_node(node) #adds node to network
        network.add_edge(node,closest_node) #adds edge between nodes

def Add_Edges(g, node, closest_node):
    # Add node to the network then add an edge
    g.add_node(node)    
    g.add_edge(node, closest_node)
    return g

def Calculate_Fitness(Development_Sites, CBD_Nodes, Road_Network, geo_t_params):
    print "Beginning"
    # Convert the sites into their coordinates    
    Dev_Nodes = Conv_2_Coords(Development_Sites, geo_t_params)
    #Add CBD and development sites to the road network
    # Gets rid of any direction restrictions
    Road_Network=Road_Network.to_undirected()
    # Add the CBD_Nodes to the road network
    Add_Nodes_To_Network(CBD_Nodes, Road_Network)
    Add_Nodes_To_Network(Dev_Nodes, Road_Network)

    print "Calculating Shortest Distances for ", len(Dev_Nodes), " sites"
    # Calcuate the shortest distance from each site to a CBD then return average    
    fdist_list = []   
    for Dev_Site in Dev_Nodes:
        shrtst_dist=10000
        for CBD in CBD_Nodes:
            try:
                dist = nx.shortest_path_length(Road_Network,Dev_Site,CBD, weight='Dist')
                if dist<shrtst_dist:
                    shrtst_dist=dist
            except nx.NetworkXNoPath:
                print "Ne path pet"
        print "Site: ", Dev_Site, " fdist = ", shrtst_dist
        fdist_list.append( shrtst_dist)
        fdist_list
    
    return fdist_list
    
    
if __name__ == '__main__': 
    
    print "Generating Sites to Calculate"
    Sites_to_Calculate  = Generate_Development_Sites(Available)
    fdist_values        =Calculate_Fitness(Sites_to_Calculate, CBD_Nodes, Road_Network, geotrans)
    
    print "Ran" 
    for x in range(0,len(fdist_values)):
        print "(", Sites_to_Calculate[x],",", fdist_values[x], "),"