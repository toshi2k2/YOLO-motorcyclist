#thanks to https://github.com/kshepard/high-risk-traffic for the reference and tutorial!
import numpy as np
import fiona
import shapely
from shapely.geometry import mapping, shape, LineString, MultiPoint, Point
from shapely.ops import transform, unary_union
import itertools
import pickle
import google_streetview.api
import google_streetview.helpers
import argparse
import streetview
import random

parser = argparse.ArgumentParser()
parser.add_argument('--sf', required=False, help='shapefile name with path to roads.shp file')
parser.add_argument('--sr', type=bool, help='save roads data if true', default=False)

parser.add_argument('--I', type=bool, default=False, help='define whether to use all roads for intersection of not - if true, then define Idata')
parser.add_argument('--Idata', type=int, default=5000, help='number of roads coordinates to be used')
parser.add_argument('--saveI', type=bool, help='save intersection data if true', default=False)
parser.add_argument('--loadI', type=bool, help='loading a intersections file pickle', default=False)
parser.add_argument('--Ifile', required=False, help='name of intersections pickle file with path')

parser.add_argument('--pan', type=bool, help='run panorama history function', default=False)

parser.add_argument('--image', type=bool, help='image download argument', default=False)
parser.add_argument('--api', required=False, help='api key', default='AIzaSyAnP2nnuWAxR3Ync0AKsUBNM6hh4axKw0w')
parser.add_argument('--size', required=False, help='size of image', default='2048x2048')
parser.add_argument('--heading', required=False, help='heading', default='0;90;180;270')
parser.add_argument('--fov', required=False, help='field of view', default='90')
parser.add_argument('--d', required=False, help='downloads folder', default='./downloads')

opt = parser.parse_args()
print(opt)

######################################################################################################################
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
######################################################################################################################
roads_shp_path = './Bangkok.osm.shp/Bangkok-shp/shape/roads.shp'

shp_file = fiona.open(roads_shp_path)
roads = []

for i,road in enumerate(shp_file):    #road is a dictionary
    if road_filter(road):
        roads.append(shape(road['geometry']))
print("number of roads: {}".format(len(roads)))

if opt.sr == True:
    with open('roads_pickle', 'wb') as f:    #quick pickle save
        pickle.dump(roads, f)

if opt.loadI == False:
    if opt.I == True:
        # random_road = random.sample(roads, opt.Idata)     #for random selection
        # # print("random", len(random_road), type(random_road))
        # intersection = get_intersections(random_road)
        intersection = get_intersections(roads[10000:10000+opt.Idata])
    else:
        intersection = get_intersections(roads)
else:
    with open(opt.Ifile, 'rb') as f:    #pickle load function for reference
        intersection = pickle.load(f)

print("number of intersections: ",len(intersection))
list_arrays = [ np.array((intersections.xy[0][0], intersections.xy[1][0])) for intersections in intersection ] #passing intersection coordinates to a list <long, lat> format

if opt.saveI == True:
    with open('intersections.txt', 'w') as f:   #writing to a file - human readable
        for item in list_arrays:
            f.write("%s\n" % item)
    #
    # with open('bangkok_intersections.txt', 'r') as f:   #opens the above file as list of string
    #     my_list = [line.rstrip('\n') for line in f]

    with open('intersections_data', 'wb') as f:    #quick pickle save
            pickle.dump(list_arrays, f)
    #
    # with open('bangkok_intersections', 'rb') as f:    #pickle load function for reference
    #     my_list = pickle.load(f)

    # print(my_list, type(my_list), type(my_list[0]))

####################################################################################################################
if opt.pan == True:
    panorama_history = []
    def panoid_history(coordinates, save=True, visual_save=False):
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

    panoid_history(list_arrays, save=True, visual_save=True)

    print(len(panorama_history), type(panorama_history[0]), panorama_history[0][0])

    def save_penoid_images(penoid_list, heading, flat_dir, key):
        """function to save penoid images"""
        for penoid_ind in penoid_list:
            streetview.api_download(penoid_ind, heading, flat_dir, key)

##################################################################################
if opt.image==True:
    list_arrays = np.vstack(list_arrays)
    list_arrays[:,[0, 1]] = list_arrays[:,[1, 0]] #exchanging columns
    # print(list_arrays)
    # print("length: ",type(list_arrays))

    list_arrays = list(map(tuple, list_arrays))
    list_arrays = [ "%s,%s" % x for x in list_arrays ]

    coordinates = ';'.join(list_arrays)
    # print(coordinates)

    apiargs = {
      'location': coordinates,#'23.87,90.3939;23.87,90.3944;23.87,90.3951;23.87,90.3959',
      'size': opt.size,
      'heading': opt.heading,
        'fov': opt.fov,
      'pitch': '0',
      'key': opt.api
    }

    # Get a list of all possible queries from multiple parameters
    api_list = google_streetview.helpers.api_list(apiargs)

    # Create a results object for all possible queries
    results = google_streetview.api.results(api_list)

    # # Preview results
    # results.preview()

    # Download images to directory 'downloads'
    results.download_links(opt.d)

    # Save metadata
    results.save_metadata('metadata.json')