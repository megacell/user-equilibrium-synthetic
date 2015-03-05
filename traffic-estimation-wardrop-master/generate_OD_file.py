# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 16:15:19 2014

@author: hugo
"""
__author__ = 'hugo.ghiron'
import numpy as np
from util import distance_on_unit_sphere, closest_node

def get_clean_ODs(nodes):
    ODs_sorted_and_filtered = filter_ODs_whithin_I210_box(sort_ODs_by_flow(create_ODs_nodes_unique(nodes)), nodes)
    return ODs_sorted_and_filtered
    
def create_ODs_nodes_unique(nodes):
    ODs_TAZ, list_TAZ, list_TAZ_ids = Read_TAZ_from_csv()
    TAZ_2_node = create_dict_TAZ_2_node(list_TAZ, list_TAZ_ids, nodes)
    ODs_nodes_multiple = []
    for od in ODs_TAZ:
        startnode, endnode = TAZ_2_node[od[0]], TAZ_2_node[od[1]]
        ODs_nodes_multiple.append([startnode, endnode, od[2]])
    ODs_nodes = sum_multiple_ODs(ODs_nodes_multiple)
    return np.asarray(ODs_nodes)
                
def Read_TAZ_from_csv(filepath_TAZ = 'Data/TAZ/Description_TAZ.csv', filepath_ODs = 'Data/ODs/CSV/CTPP_LA.csv'):
    list_TAZ = np.genfromtxt(filepath_TAZ, delimiter=',', skip_header = 1)
    list_TAZ_ids = list_TAZ[:,0].astype(int)
    flows = []
    i=0
    with open(filepath_ODs, 'rb') as f:
        for line in f:
			l = line.split('\",\"')
			i=i+1
			tazi = int( l[0].split(',')[0].split(' ')[1]) # parsed TAZ_id
			tazi = int(-20000+tazi/1000)
			tazj = int(l[1].split(',')[0].split(' ')[1]) # parsed TAZ_id
			tazj = int(-20000+tazj/1000)	
			if (tazi in list_TAZ_ids and tazj in list_TAZ_ids):
				f = float(l[4].replace(',','')) + float(l[6].replace(',',''))/2.0 + float(l[8].replace(',',''))/3.0 + float(l[10].replace(',',''))/4.0 + float(l[12].replace(',',''))/5.0 + float(l[14].replace(',',''))/6.0     # total vehicle-trips, we divide when people are a lot in cars
				if (f!=0 and tazi !=tazj):				
					flows.append([tazi, tazj, float(f)])
    return np.asarray(flows), list_TAZ, list_TAZ_ids

def create_dict_TAZ_2_node(List_TAZ, List_TAZ_ids, nodes):
    dict = {}
    for j in range(len(List_TAZ_ids)): 
        i = List_TAZ_ids[j]
        dict[i] = closest_node(List_TAZ[j][1], List_TAZ[j][2], nodes)
    return dict

def sum_multiple_ODs(ODs_multiple, division_factor = 5):
    #Our ODs represent the ODs for the whole morning peak. Since this occurs for many hours we have to devide by the average number of hours 
    division_factor = 2.5 #if we want to try something else than 5
    dict_unique = {}
    ODs_unique = []
    for od in ODs_multiple:
        if od[0]!=od[1]:
            if dict_unique.has_key((od[0], od[1])):
                dict_unique[(od[0], od[1])] += od[2]/division_factor 
            else : dict_unique[(od[0], od[1])] = od[2]/division_factor
    for od, value in dict_unique.iteritems():
        ODs_unique.append([od[0], od[1], value])
    return ODs_unique

def sort_ODs_by_flow(ODs_unsorted):
    def Get_key(item):
        return item[2]
    ODs_sorted = np.asarray(sorted(ODs_unsorted, key = Get_key))
    return ODs_sorted
    
def filter_ODs_whithin_I210_box(ODs_list, nodes_list):
    nodes = nodes_list
    temp = ODs_list
    ODs_sorted = []
    for od in temp:
        startnode = nodes[od[0]-1]
        endnode = nodes[od[1]-1]
        ODs_sorted.append([od[0], od[1], od[2], distance_on_unit_sphere(nodes[od[0]-1][1], nodes[od[0]-1][0], nodes[od[1]-1][1], nodes[od[1]-1][0]), Is_in_I210box(startnode[1], startnode[0], 'medium'), Is_in_I210box(endnode[1], endnode[0], 'medium')])
    ODs_sorted = np.asarray(ODs_sorted)
    print ODs_sorted[0:20]
    temp = ODs_sorted
    ODs_sorted  = []
    for od in temp:
        if od[4]+od[5]>1 : ODs_sorted.append(od[0:4])
    return np.asarray(ODs_sorted)

def Is_in_I210box(lat, lng, type = 'box'):
    if type == 'box' :box = [34.124918, 34.1718, -118.1224, -118.02524]
    if type == 'medium' : box = [34.081133, 34.237951, -118.249853, -117.893484]
    return (lat < box[1] and lat > box[0] and lng < box[3] and lng > box[2])

def write_OD_textfile_in_cpp_format(clean_ODs, filename):

    n_zones = count_total_origins_or_dests(clean_ODs)
    total_flow = np.sum(clean_ODs[:,2])
    def Get_key(item): return item[0] #sort by the origin
    ODs_sorted = np.asarray(sorted(clean_ODs, key = Get_key))
    
    def write_new_origin_as_string(i):
        current_origin = ODs_sorted[i][0]
        text_file.write('Origin '+str(int(current_origin))+'\n')
        return current_origin    
    
    text_file = open('../M_Steel_solver/networks/OSM_medium/'+filename, "w")
    text_file.write('<NUMBER OF ZONES> '+str(n_zones)+'\n')
    text_file.write('<TOTAL OD FLOW> '+str(total_flow)+'\n')
    text_file.write('<END OF METADATA>\n')
    text_file.write('\n')
    i, current_origin = 0, -1
    list_of_ODs_per_origin_as_string = ''
    while(i < len(clean_ODs)):
        od = ODs_sorted[i]
        if od[0] != current_origin:
            if i != 0: 
                print list_of_ODs_per_origin_as_string
                text_file.write(list_of_ODs_per_origin_as_string+'\n')
            current_origin = write_new_origin_as_string(i)
            list_of_ODs_per_origin_as_string = '\t'+str(int(od[1]))+' :\t'+str(od[2])+';'
        else: 
            list_of_ODs_per_origin_as_string += '\t'+str(int(od[1]))+' :\t'+str(od[2])+';'
        if i == len(clean_ODs) - 1:
            text_file.write(list_of_ODs_per_origin_as_string)
        i += 1   
    return n_zones
    
def count_total_origins_or_dests(ODs_list):
    dict = {}
    for od in ODs_list:
        if not dict.has_key(od[0]):
            dict[od[0]] = 1
        if not dict.has_key(od[1]):
            dict[od[1]] = 1
    return len(dict.items())
    
def main():
    nodes = np.genfromtxt('Data/Network/CSV/LA_big_box_arterials/nodes_LA_toy.csv', delimiter = ',', skiprows = 1)
    nodes = nodes[:,1:3]
    clean_ODs = sort_ODs_by_flow(create_ODs_nodes_unique(nodes))
    n_zones = write_OD_textfile_in_cpp_format(clean_ODs, 'ODs.txt')
    print 'n_zones = '+str(n_zones)

if __name__ == '__main__':
    main()