import numpy as np

# with open('bangkok_intersections.txt', 'r') as f:   #opens the above file as list of string
#     my_list = [line.rstrip('\n') for line in f]

my_list = np.genfromtxt(r'bangkok_intersections.txt')
my_list[:,[0, 1]] = my_list[:,[1, 0]] #exchanging columns
print(my_list.shape)
print("length: ",len(my_list))
import google_streetview.api
import google_streetview.helpers
# print(my_list[9000])

# my_list = my_list[0:1]

my_list = list(map(tuple, my_list))
my_list = [ "%s,%s" % x for x in my_list ]

# print(my_list)
coordinates = ';'.join(my_list)
# print(coordinates)


# my_list = my_list[0:10]
#
# my_list = list(map(tuple, my_list))
# my_list = [ "%s,%s" % x for x in my_list ]
#
# # print(my_list[0])
# # my_list = my_list[]
# # print(my_list)
# # coordinates = ';'.join(my_list)
# # print(coordinates)
#
# # from itertools import chain
# # tup = my_list[0]
# # myString = str(tup)
# # print(myString)
# for ind in range(len(my_list)):
#     tup = my_list[ind]
#     coordinates = str(tup)
#     print(coordinates)
#     params = [{
#       'size': '400x400', # max 640x640 pixels
#       'location': coordinates,
#       'heading': 0,
#       'pitch': '0',
#       'key': ''
#     }]
#
#     # Create a results object
#     results = google_streetview.api.results(params)
#
#     # # Preview results
#     # results.preview()
#
#     # Download images to directory 'downloads'
#     results.download_links('./downloads{}'.format(ind))
#
#     # Save links
#     results.save_links('links.txt')
#
#     # Save metadata
#     results.save_metadata('metadata.json')

# apiargs = {
#   'location': coordinates,#'',
#   'size': '400x400',
#   'heading': '0;90;180;270',
#     'fov': '90',
#   'pitch': '0',
#   'key': ''
# }
#
# # Get a list of all possible queries from multiple parameters
# api_list = google_streetview.helpers.api_list(apiargs)
#
# # Create a results object for all possible queries
# results = google_streetview.api.results(api_list)
#
# # # Preview results
# # results.preview()
#
# # Download images to directory 'downloads'
# results.download_links('./downloads_bangkok')
#
# # Save metadata
# results.save_metadata('metadata.json')
