# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:41:06 2015

@author: hugo
"""
__author__ = 'hugo.ghiron' 

import numpy as np
import csv

def transform_cpp_output_to_jason_format(clean_links, nodes, filepath = '../M_Steel_solver/output.txt'): 
    cpp_output = read_network_flows_from_cpp_output(filepath)
    write_output_in_Jason_format(clean_links, nodes, cpp_output)

def read_network_flows_from_cpp_output(filepath = '../M_Steel_solver/output.txt'):
    variable = np.genfromtxt(filepath, delimiter = '\t', skiprows = 6)   
    origins = variable[:,1]
    dests = variable[:,2]
    flows = variable[:,4]
    links = np.vstack((origins, dests, flows)).T
    return links

def write_output_in_Jason_format(clean_links, nodes, output_cpp):
    with open('output_for_Jason.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter = ';')
        writer.writerow(['lng1', 'lat1', 'lng2', 'lat2', 'flow/capacity', 'travel_time/fftt', 'capacity'])
        for i in range(len(output_cpp)):
            link_output = output_cpp[i]
            link_input = clean_links[i]
            lng1, lat1, lng2, lat2 = nodes[link_output[0]-1][0], nodes[link_output[0]-1][1], nodes[link_output[1]-1][0], nodes[link_output[1]-1][1]
            cap = 1/link_input[4][1]
            flow = link_output[2]
            ratio_travel_times = 1 + 0.15*np.power(flow/cap,4)
            writer.writerow([lng1, lat1, lng2, lat2, flow/cap, ratio_travel_times, cap]) 