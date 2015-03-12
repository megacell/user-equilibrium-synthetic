# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:41:06 2015

@author: hugo
"""
__author__ = 'hugo.ghiron' 

import numpy as np
import csv

def transform_cpp_output_to_jason_format(clean_links, nodes, osm_source = False, dict_link_2_attributes = {}, filepath = '../M_Steel_solver/output.txt'): 
    cpp_output = read_network_flows_from_cpp_output(filepath)
    write_output_in_Jason_format(clean_links, nodes, cpp_output, osm_source, dict_link_2_attributes)

def read_network_flows_from_cpp_output(filepath = '../M_Steel_solver/output.txt'):
    variable = np.genfromtxt(filepath, delimiter = '\t', skiprows = 6)   
    origins = variable[:,1]
    dests = variable[:,2]
    flows = variable[:,4]
    links = np.vstack((origins, dests, flows)).T
    return links

def write_output_in_Jason_format(clean_links, nodes, output_cpp, osm_source, dict_link_2_attributes):
    with open('output_for_Jason.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter = ';')
        if osm_source == False:
            writer.writerow(['lng1', 'lat1', 'lng2', 'lat2', 'flow/capacity', 'travel_time/fftt', 'capacity'])
            for i in range(len(output_cpp)):
                link_output = output_cpp[i]
                link_input = clean_links[i]
                lng1, lat1, lng2, lat2 = nodes[link_output[0]-1][0], nodes[link_output[0]-1][1], nodes[link_output[1]-1][0], nodes[link_output[1]-1][1]
                cap = 1/link_input[4][1]
                flow = link_output[2]
                ratio_travel_times = 1 + 0.15*np.power(flow/cap,4)
                writer.writerow([lng1, lat1, lng2, lat2, flow/cap, ratio_travel_times, cap])
        else:
            writer.writerow(['lng1', 'lat1', 'lng2', 'lat2', 'flow/capacity', 'travel_time/fftt', 'capacity', 'freespeed', 'length', 'fftt'])
            for i in range(len(output_cpp)):
                lost_flow = 0
                link_output = output_cpp[i]
                lng1, lat1, lng2, lat2 = nodes[link_output[0]-1][0], nodes[link_output[0]-1][1], nodes[link_output[1]-1][0], nodes[link_output[1]-1][1]
                if dict_link_2_attributes.has_key((link_output[0], link_output[1])) == False:
                    print str((link_output[0], link_output[1])) + 'not in initial dict'
                    lost_flow += link_output[2]
                else: 
                    cap, freespeed, length, ff_d = dict_link_2_attributes[(link_output[0], link_output[1])]
                    flow = link_output[2]
                    ratio_travel_times = 1 + 0.15*np.power(flow/cap,4)
                    writer.writerow([lng1, lat1, lng2, lat2, flow/cap, ratio_travel_times, cap, freespeed, length, ff_d])
            print 'total flow lost because of the new links not in the initial dict = '+ str(lost_flow)