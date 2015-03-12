# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:31:47 2015

@author: hugo
"""
__author__ = 'hugo.ghiron'

import numpy as np
from cvxopt import matrix
from util import distance_on_unit_sphere, is_in_box

def get_clean_links(nodes=None, delaytype = 'Polynomial', parameters = matrix([0.0, 0.0, 0.0, 0.15])):
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

def get_clean_links_from_OSM_raw_links(nodes, raw_links, delaytype='Polynomial', parameters = matrix([0.0, 0.0, 0.0, 0.15])):
    #To simulate an incident one can change a capacity right here    
    tmp = raw_links
    clean_links=[]
    if delaytype=='Polynomial':
        theta = parameters
        degree = len(theta)
        for startnode, endnode, route, ffdelay, slope in tmp:
            coef = [ffdelay*a*b for a,b in zip(theta, np.power(slope, range(1,degree+1)))]
            clean_links.append((startnode, endnode, route, ffdelay, (ffdelay, slope, coef))) 
    return clean_links

def extract_raw_nodes_links_from_box(latmin=33.0, latmax=36.0, lngmin=-120.0, lngmax=-116.0):
    '''One needs to transform a qgis file into a csv with all the attributes. This method reads this csv file
    '''
    dict = {}
    node_data = np.genfromtxt('Data/Network/CSV/LA_small_box_detailed/nodes_la_exported2.csv', delimiter = ';', skiprows=1)
    nodes_table=[]
    osmId_2_gId = {}
    k = 1
    for i in range(len(node_data)):
        node=[node_data[i][0], node_data[i][1], node_data[i][2]]
        if is_in_box(latmin, latmax, lngmin, lngmax, node):
            nodes_table.append([node[0], node[1]])    
            osmId_2_gId[int(node[2])] = k # osmId_2_gId[int(osmId)] = gId
            k += 1
    #print str(osmId_2_gId[1687115183])+ ' this is the dest'
    link_data = np.genfromtxt('Data/Network/CSV/LA_small_box_detailed/links_la_exported.csv', delimiter = ',', skiprows=1)
    link_table=[]
    for i in range(len(link_data)):
        sn, en=int(link_data[i][1]), int(link_data[i][2])
        if (sn in osmId_2_gId.keys() and en in osmId_2_gId.keys()):
            startnode = osmId_2_gId[sn]
            endnode = osmId_2_gId[en]
            length = link_data[i][3]
            cap = link_data[i][5]
            freespeed = link_data[i][6]
            ff_d=length/freespeed
            #slope= 2000 / cap
            slope= 1 / cap
            u=[startnode,endnode,1,ff_d,slope]
            link_table.append(u)
            dict[(startnode, endnode)] = (cap, freespeed, length, ff_d)
    link_table_without_double = kill_double_links(link_table)
    return nodes_table, link_table_without_double, dict
         
def kill_double_links(links_list):
    links_without_double=[]
    counter=0
    for i in range(len(links_list)):
        link=links_list[i]
        startnode,endnode=link[0], link[1]
        flag=True
        for j in range(len(links_list)-i-1):
            link_j=links_list[j+i+1]
            if (startnode==link_j[0] and endnode == link_j[1]): flag=False
        if (flag==True): links_without_double.append(link)
        else: counter+=1
    print str(counter)+' links removed'
    return links_without_double

def write_network_file_in_cpp_format(clean_links,n_zones, n_nodes):
    text_file = open("../M_Steel_solver/networks/OSM_medium/OSM_medium_net.txt", "w")
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
    
def main(osm_source = False):
    n_zones = -1
    
    if osm_source == False:
        #If UE on a hand network:
        nodes = np.genfromtxt('Data/Network/CSV/LA_big_box_arterials/nodes_LA_toy.csv', delimiter = ',', skiprows = 1)
        nodes = nodes[:,1:3]
        clean_links = get_clean_links(nodes)
    else:   
        #If UE on a OSM-source network:
        box = [33.0, 36.0, -120.0, -116.0]
        nodes, raw_links = extract_raw_nodes_links_from_box(box[0], box[1], box[2], box[3])
        clean_links = get_clean_links_from_OSM_raw_links(nodes, raw_links)
    
    write_network_file_in_cpp_format(clean_links,n_zones, len(nodes))
    
if __name__ == '__main__':
    main()