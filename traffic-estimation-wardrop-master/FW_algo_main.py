# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:27:13 2015

@author: hugo
"""
__author__ = 'hugo.ghiron'

import numpy as np
import subprocess

import generate_OD_file as od
import generate_network_file as nw
import transform_output as t
import graph as g
import draw_graph as d

def main():
    nodes = np.genfromtxt('Data/Network/CSV/LA_big_box_arterials/nodes_LA_toy.csv', delimiter = ',', skiprows = 1)
    nodes = nodes[:,1:3]
    
    #Create the OD-file for the Frank Wolfe algorithm from the csv files of the TAZ and the Census ODs.
    print 'Creating OD-file'    
    clean_ODs = od.sort_ODs_by_flow(od.create_ODs_nodes_unique(nodes))
    n_zones = od.write_OD_textfile_in_cpp_format(clean_ODs, 'OSM_medium_trips.txt')
    
    #Create the networks-file from the csv files of our networks for the Frank Wolfe algorithm
    print 'Creating network-file'       
    clean_links = nw.get_clean_links(nodes)
    nw.write_network_file_in_cpp_format(clean_links, n_zones, len(nodes))
    
    #Run the code from M. Steel
    print 'Running FW algorithm'    
    #!/usr/bin/python
    result = subprocess.check_output(["/bin/bash", "bash_instructions_to_run_FW.txt"])
    print result
    
    #Transform the output from Cpp's format into a suitable format for Jason's visualization
    t.transform_cpp_output_to_jason_format(clean_links, nodes)
    
    #Visualize the output on Jerome's visu
    print 'Creating graph for visu'    
    graph = g.create_graph_from_list(nodes, clean_links, 'Polynomial', [], 'Larger map of L.A.')
    cpp_output = t.read_network_flows_from_cpp_output()
    graph.update_linkflows_from_cpp_output(cpp_output)
    d.draw_delays(graph)

if __name__ == '__main__':
    main()