'''
filename: circles.py
author: bancks holmes
usage: accepts a list of latitudes and longitudes from a csv file and spits out a list of  geojson with
20-sided polygons drawn around each point. This project began life to make an assignment in
dci-102 easier and is similar to airport-radius.py
'''

'''
to do:
-optimize! this thing always crashes my shit
-find the source that the meat of the project came from
-reformat using oop concepts
    --use obj class with init and str methods
-generalize to cli and arg0 = input filename, arg1 = lat field, arg2 = long field, arg3 = radius,
arg4 = output filename
    --maybe use a gui at this point?
'''

import shapely.geometry
import json
import geog
import numpy as np
import pandas as pd

def make_polygon(coords):
    '''coords: an ordered pair of coordinates (lat, long)
    that represent the center of the city'''
    p = shapely.geometry.Point([coords[0], coords[1]])
    n_points = 20
    d = 100 * 1609
    angles = np.linspace(0, 360, n_points)
    polygon = geog.propagate(p, angles, d)
    return json.dumps(shapely.geometry.mapping(shapely.geometry.Polygon(polygon)))

def make_cities_list():
    df = pd.read_csv('airports_lat_long.csv')
    needed_columns = df[['city', 'lat', 'lng']]
    i = 0
    end_list = []
    for idx, row in needed_columns.iterrows():
        end_list.append([row[0], row[1], row[2]])
        i += 1
    return end_list                      
    

def main():
    cities = make_cities_list()
    start_str = '{"type": "FeatureCollection","features": ['
    obj_start_str = '{"type": "Feature","geometry":'
    obj_end_str = ',"properties": {"this_script": "sucks","additionally": { "it_was": "hard_to_write" }}},'
    end_str = ']}'
    full_str = start_str
    for city in cities:
        full_str += obj_start_str
        full_str += str(make_polygon((city[2], city[1])))
        full_str += obj_end_str
    full_str += end_str
    make_cities_list()
    print(full_str)  #change this to write to file
        

if __name__ == '__main__':
    main()
