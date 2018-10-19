# YOLO-motorcyclist
Code for collection and creation of image dataset for training an new version of YOLO architecture, in order to identify motorcyclists with/without helmets.
First, shapefiles are read and road intersection coordinates are collected, which are used to get panoids (over the years) as well as images from Google Street View with respective FOV, Heading, etc.
Collect data by using image_data_generation.py file by running following commands:

Download your shapefile and put the roads.shp file in folder called data
$ pip install -r requirements.txt
$ python combine.py --sf ./data/roads.shp --sr True --saveI True --image True
Run the help function to see all functionalities
