import numpy as np
# import fiona
# import shapely
# from shapely.geometry import mapping, shape, LineString, MultiPoint, Point
# from shapely.ops import transform, unary_union
# import itertools
import pickle
import google_streetview.api
import google_streetview.helpers
import argparse
import streetview
import random
import math
import os

parser = argparse.ArgumentParser()
parser.add_argument('--Ifile', required=False, help='name of intersections pickle file with path')
parser.add_argument('--image', type=bool, help='image download argument', default=False)
parser.add_argument('--api', required=False, help='api key', default='')
parser.add_argument('--size', required=False, help='size of image', default='2048x2048')
parser.add_argument('--heading', required=False, help='heading', default='0;90;180;270')
parser.add_argument('--fov', required=False, help='field of view', default='90')
parser.add_argument('--d', required=False, help='downloads folder', default='./')  # change to /d

opt = parser.parse_args()
print(opt)

with open(opt.Ifile, 'rb') as f:    #pickle load function for reference
    intersection = pickle.load(f)

print("number of coordinates: ",len(intersection))
# list_arrays = [ np.array((intersections.xy[0][0], intersections.xy[1][0])) for intersections in intersection ] #passing intersection coordinates to a list <long, lat> format

if opt.image==True:
    # list_arrays = np.vstack(intersection)
    # list_arrays[:,[0, 1]] = list_arrays[:,[1, 0]] #exchanging columns
    # print(list_arrays)
    # print("length: ",type(list_arrays))

    total_arrays = [tuple(d.values()) for d in intersection]

    for i in range(0,math.ceil(len(total_arrays)/5000)):
        if len(total_arrays)>i*5000+5000:
            sub_array = total_arrays[i*5000:i*5000+5000]
        else:
            sub_array = total_arrays[i*5000:-1]

        list_arrays = [ "%s,%s" % x for x in sub_array ]
        # print(list_arrays, type(list_arrays), type(list_arrays[0]))

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
        # print(len(api_list), type(api_list), api_list[0])

        # Create a results object for all possible queries
        results = google_streetview.api.results(api_list)

        # # Preview results
        # results.preview()

        # Download images to directory 'downloads'
        opt.d = opt.d + opt.Ifile[:-6] + str(i)
        try:  
            os.mkdir(opt.d)
        except OSError:  
            print ("Creation of the directory %s failed" % opt.d)

        results.download_links(opt.d)

        # Save metadata
        results.save_metadata('metadata.json')
