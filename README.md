# YOLO-motorcyclist
Code for collection and creation of image dataset for training an new version of YOLO architecture, in order to identify motorcyclists with/without helmets.
First, shapefiles are read and road intersection coordinates are collected, which are used to get panoids (over the years) as well as images from Google Street View with respective FOV, Heading, etc.
Collect data by using image_data_generation.py file by running following commands:
$ pip install -r requirements.txt

usage: image_data_generation.py [-h] --sf SF [--sr SR] [--I I] [--Idata IDATA]
                                [--saveI SAVEI] [--loadI LOADI]
                                [--Ifile IFILE] [--pan PAN] [--image IMAGE]
                                [--api API] [--size SIZE] [--heading HEADING]
                                [--fov FOV] [--d D]

optional arguments:
  -h, --help         show this help message and exit
  --sf SF            shapefile name with path
  --sr SR            save roads data if true
  --I I              define whether to use all roads for intersection of not -
                     if true, then define Idata
  --Idata IDATA      number of roads coordinates to be used
  --saveI SAVEI      save intersection data if true
  --loadI LOADI      loading a intersections file pickle
  --Ifile IFILE      name of intersections pickle file with path
  --pan PAN          run panorama history function
  --image IMAGE      image download argument
  --api API          api key
  --size SIZE        size of image
  --heading HEADING  heading
  --fov FOV          field of view
  --d D              downloads folder
