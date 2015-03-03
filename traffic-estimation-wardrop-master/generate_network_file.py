# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:31:47 2015

@author: hugo
"""
__author__ = 'hugo.ghiron'

import numpy as np
from cvxopt import matrix
from util import distance_on_unit_sphere

def get_clean_links(nodes, delaytype = 'Polynomial', parameters = matrix([0.0, 0.0, 0.0, 0.15])):
    links = np.genfromtxt('Data/Network/CSV/LA_big_box_arterials/links_qgis_cap.csv', delimiter = ',', skiprows = 1)
    tmp = links
    links = []
    speed_limit_freeway = 33.33 #unit: m/s
    dict_cap2speed ={600:12.5, 1000:16.67, 2000:16.67, 4000:16.67, 5000:16.67, 1500:16.67, 3000:22.22, 6000:22.22, 9000:22.22, 4500:22.22, 7500:22.22, 10500:22.22}
    
    if delaytype=='None':
        for startnode, endnode, category in tmp:
            arc = distance_on_unit_sphere(nodes[startnode-1][2], nodes[startnode-1][1], nodes[endnode-1][2], nodes[endnode-1][1])
            if category == 1: ffdelay = arc/speed_limit_freeway
            if category == 2: ffdelay = arc/16.67
            if category !=0: links.append((startnode, endnode, 1, ffdelay, None))
            
    if delaytype=='Polynomial':
        theta = parameters
        degree = len(theta)
        for startnode, endnode, category, cap in tmp:
            arc = distance_on_unit_sphere(nodes[startnode-1][1], nodes[startnode-1][0], nodes[endnode-1][1], nodes[endnode-1][0])
            if category == 1: ffdelay, slope = arc/speed_limit_freeway, 1/cap
            if category == 2: 
                if dict_cap2speed.has_key(cap): 
                    ffdelay, slope = arc/dict_cap2speed[cap], 1/cap
                else : ffdelay, slope = arc/16.67, 1/cap
            coef = [ffdelay*a*b for a,b in zip(theta, np.power(slope, range(1,degree+1)))]
            links.append((startnode, endnode, 1, ffdelay, (ffdelay, slope, coef)))
    return links

def write_network_file_in_cpp_format(clean_links,n_zones, n_nodes):
    text_file = open("/home/hugo/Desktop/Hugo/Code/M_Steel_solver/networks/OSM_medium/OSM_medium_net.txt", "w")
    text_file.write('<NUMBER OF ZONES> '+str(n_zones)+'\n')
    text_file.write('<NUMBER OF NODES> '+str(n_nodes)+'\n')
    text_file.write('<FIRST THRU NODE> 1\n') #I haven't fully understood this parameter yet (Hugo)
    text_file.write('<NUMBER OF LINKS> '+str(len(clean_links))+'\n')
    text_file.write('<END OF METADATA>\n')
    text_file.write('~ Init/Term/Cap/Length/FreeFlowTime/B=0.15/Power=4/Speed limit/Toll/Type;\n')
    text_file.write('\n')
    for link in clean_links:
        startnode, endnode, cap, free_flow_delay = link[0], link[1], 1/link[4][1], link[3]
        line_str = str(int(startnode))+'\t'+str(int(endnode))+'\t'+str(int(cap))+'\t'+str(0)+'\t'+str(free_flow_delay)+'\t'+str(0.15)+'\t'+str(4)+'\t'+str(25)+'\t'+str(0)+'\t'+str(3)+'\t;'        
        text_file.write(line_str+'\n')  
    
def main():
    nodes = np.genfromtxt('Data/Network/CSV/LA_big_box_arterials/nodes_LA_toy.csv', delimiter = ',', skiprows = 1)
    nodes = nodes[:,1:3]
    clean_links = get_clean_links(nodes)
    n_zones = 189 #To be made automatic !!!
    write_network_file_in_cpp_format(clean_links,n_zones, len(nodes))
    
if __name__ == '__main__':
    main()