image_data_generation.py file by running following commands:
Download your shapefile and put the roads.shp file in folder called data in the current directory.

$ pip install -r requirements.txt
$ python combine.py --sf ./data/roads.shp --sr True --saveI True --image True
Run the help function to see all functionalities.
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


for e.g.
$ python combine.py --sf ./data/roads.shp --sr True --I True --Idata 1000 --saveI True --image True
There is a data with Bangkok road shapefile in this code folder. Try running that.