#thanks to https://github.com/kshepard/high-risk-traffic for the reference and tutorial!
import numpy as np
import fiona
import shapely
from shapely.geometry import mapping, shape, LineString, MultiPoint, Point
from shapely.ops import transform, unary_union
import itertools
import pickle


def road_filter(road):        #use this function to remove certain type of characteristics; for e.g.
    if ('highway' in road['properties']
            and road['properties']['highway'] is not None
            and road['properties']['highway'] != 'path'
            and road['properties']['highway'] != 'footway'):
        return True
    if ('class' not in road['properties'] or road['properties']['class'] == 'highway'
            and road['properties']['bridge'] == 0
            and road['properties']['tunnel'] == 0):
        return True
    return False

def get_intersections(roads):
    intersections = []
    for road1, road2 in itertools.combinations(roads, 2):
        if road1.intersects(road2):
            intersection = road1.intersection(road2)
            if 'Point' == intersection.type:
                intersections.append(intersection)
            elif 'MultiPoint' == intersection.type:
                intersections.extend([pt for pt in intersection])
            elif 'MultiLineString' == intersection.type:
                multiLine = [line for line in intersection]
                first_coords = multiLine[0].coords[0]
                last_coords = multiLine[len(multiLine)-1].coords[1]
                intersections.append(Point(first_coords[0], first_coords[1]))
                intersections.append(Point(last_coords[0], last_coords[1]))
    return unary_union(intersections)

roads_shp_path = './Bangkok.osm.shp/Bangkok-shp/shape/roads.shp'

shp_file = fiona.open(roads_shp_path)
roads = []

for i,road in enumerate(shp_file):    #road is a dictionary
    # if i % 10000 == 0:
    if i == 1:
        # print(road.keys())           #dict_keys(['type', 'id', 'geometry', 'properties'])

        # print(road.values())
        """dict_values(['Feature', '1', {'type': 'LineString', 'coordinates': 
        [(100.5272629, 13.7515891), (100.5270537, 13.7516305), (100.5261941, 13.7518009), (100.5259472, 13.7518498), 
        (100.5256738, 13.751904)]}, OrderedDict([('osm_id', 8560761), ('name', None), ('ref', None), 
        ('type', 'residential'), ('oneway', 0), ('bridge', 0), ('maxspeed', None)])])"""

        # print(road.items())
        """dict_items([('type', 'Feature'), ('id', '1'), ('geometry', {'type': 'LineString', 'coordinates': 
        [(100.5272629, 13.7515891), (100.5270537, 13.7516305), (100.5261941, 13.7518009), (100.5259472, 13.7518498), 
        (100.5256738, 13.751904)]}), ('properties', OrderedDict([('osm_id', 8560761), ('name', None), ('ref', None), 
        ('type', 'residential'), ('oneway', 0), ('bridge', 0), ('maxspeed', None)]))])"""
        # print(road,'\n')
        # print(type(road))
        pass

    if road_filter(road):
        roads.append(shape(road['geometry']))
        # if i % 10000 == 0:
        #     print(road['geometry'], '\n')
# print(roads[1])
# print(i, len(roads))

intersection = get_intersections(roads[1:100])
list_arrays = [ np.array((intersections.xy[0][0], intersections.xy[1][0])) for intersections in intersection ] #passing intersection coordinates to a list <long, lat> format
# print(type(intersection), len(intersection), intersection[0])
# for array in list_arrays:
#     print(array)
with open('bangkok_intersections.txt', 'w') as f:   #writing to a file - human readable
    for item in list_arrays:
        f.write("%s\n" % item)
#
# with open('bangkok_intersections.txt', 'r') as f:   #opens the above file as list of string
#     my_list = [line.rstrip('\n') for line in f]

# with open('bangkok_intersections', 'wb') as f:    #quick pickle save
#     pickle.dump(list_arrays, f)
#
# with open('bangkok_intersections', 'rb') as f:    #pickle load function
#     my_list = pickle.load(f)

# print(my_list, type(my_list), type(my_list[0]))

import streetview

panorama_history = []
def panoid_history(coordinates, save=False, visual_save=False):
    """This function is for getting the panoids of panorimic views from Google Street View
    as a function of multiple years and  months"""
    for long,lat in coordinates:
        # print("lat:", lat)
        panoids = streetview.panoids(lat=lat, lon=long)
        panorama_history.append(panoids)

    if save:
        with open('panorama_hitorical_pickle', 'wb') as f:
            pickle.dump(panorama_history, f)

    if visual_save:
        with open('panorama_history.txt', 'w') as f:  # writing to a file - human readable
            for item in panorama_history:
                f.write("%s\n" % item)

# with open('panorama_hitorical_pickle', 'rb') as f:    #pickle load function
#     pano_list = pickle.load(f)

panoid_history(list_arrays, save=False, visual_save=False)

print(len(panorama_history), type(panorama_history[0]), panorama_history[0][0])

def save_penoid_images(penoid_list, heading, flat_dir, key):
    """function to save penoid images"""
    for penoid_ind in penoid_list:
        streetview.api_download(penoid_ind, heading, flat_dir, key)