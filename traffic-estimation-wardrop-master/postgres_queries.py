# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 11:00:47 2014

@author: Hugo
"""

'''
The purpose of this class is to transform the TAZ in a shapefile format into a CSV file depicting the centroid of each TAZ. The main file (FW_algo_main) will take this csv TAZ file as input for the algorithm. 
The TAZ file has to be loaded already into Postgres)

Be Careful if you are using this file for elsewhere than LA. You should then change the functions is_in_LA_box, and filter_taz_LA_county, and the UTM identification in the derive_taz_attributes function.
'''

__author__ = 'hugo.ghiron'
import psycopg2
import utm 
#https://pypi.python.org/pypi/utm
#To know the UTM you're dealing with: uncomment below
#print utm.from_latlon(lat_test, lng_test)
#For Los Angeles, utm.from_latlon(34, -118) = 11, N
import csv

def is_in_LA_Box(lat, lng):
    latmax, latmin, lngmax, lngmin = 34.288621 , 33.9185, -117.646497, -118.394048
    if (lat < latmax and lat > latmin and lng < lngmax and lng > lngmin): return True
    else : return False

def filter_taz_LA_county(cur):
    list_taz_LA_county=[]
    s='select TAZ.gid from taz_boundary_scag_2009 TAZ where TAZ.county = \'037\''
    #The county #37 corresponds to the county of interest for LA (Los Angeles County). Change it accordingly for studying other cities or areas.
    cur.execute(s)
    rows=cur.fetchall()
    for row in rows:
        list_taz_LA_county.append(int(str(row[0])))
    return list_taz_LA_county

def derive_taz_attributes(cur, list_taz):
    
    description_taz=[]
    for taz_id in list_taz:
        
        s='select ST_AsText(ST_Centroid(TAZ.geom)) from taz_boundary_scag_2009 TAZ where TAZ.gid = '+str(taz_id)+';'
        cur.execute(s)
        rows=cur.fetchall()
        for row in rows:
            pos_centroid_UTM = (str(row[0]))
            pos_centroid_UTM = pos_centroid_UTM[6:len(pos_centroid_UTM)-1]
            pos_centroid_UTM = pos_centroid_UTM.split()
            pos_centroid_UTM = map(float, pos_centroid_UTM)
            lat_centroid, lng_centroid = utm.to_latlon(pos_centroid_UTM[0], pos_centroid_UTM[1] , 11, 'N') #The shapefiles are in the UTM "11N" coordinates
    
        if is_in_LA_Box(lat_centroid, lng_centroid):
            s='select count(*) from taz_boundary_scag_2009 TAZ, la_network_nodes_v2 nodes where TAZ.gid = '+str(taz_id)+' AND ST_Contains(TAZ.geom, nodes.geom);'
            cur.execute(s)
            rows=cur.fetchall()
            for row in rows:
                nb_nodes_in_taz = int(str(row[0]))
            s='select TAZ.area_ from taz_boundary_scag_2009 TAZ where TAZ.gid = '+str(taz_id)+';'
            cur.execute(s)
            rows=cur.fetchall()
            for row in rows:
                area_taz = float(str(row[0]))
        
            description_taz.append([taz_id, lat_centroid, lng_centroid, nb_nodes_in_taz, area_taz])
            
    return description_taz

def write_TAZ_file_as_csv(description_taz):
    with open('Data/TAZ/Description_TAZ.csv', 'wb') as csvfile:
        c = csv.writer(csvfile, delimiter=',')
        c.writerow(["TAZ_id", "Lat_centroid","Lng_centroid","Nb_nodes_in_Taz","Area_taz"])
        for row in description_taz:
            c.writerow(row)
   
def main():
    #Put your connection IDs here, and modify the next line
    conn = psycopg2.connect("dbname='ca_census' user='postgres' host='localhost' password=''")
    cur = conn.cursor()
    list_taz = filter_taz_LA_county(cur)
    description_taz = derive_taz_attributes(cur, list_taz)
    write_TAZ_file_as_csv(description_taz)
         
if __name__ == '__main__':
    main()