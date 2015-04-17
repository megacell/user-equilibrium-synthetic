How to run the Frank-Wolfe solver
====================

This tool allows to compute the User-Equilibrim on large networks. One runs the script from Python and the C++ Frank-Wolfe code is called.
-------------------------------
0.	Pull the repo
1.	Choose the right makefile
2.	Compile
3.	Run the experiments
4. 	Generating the input files for other cities

Pull the repo
-------------------------------
Pull the repo https://github.com/megacell/user-equilibrium-synthetic

Choose the right makefile
-------------------------------

It's not the same makefile if you are working on Linux of on Mac OS. Unfortunately this tool doesn't work on Windows. 
The 'Makefile_linux' is the one for Linux, and the 'Makefile_Mac_OS' is for Mac_OS.

Compile
-------------------------------

You can open the EquilibriumFlow.cpp file at the path : M_Steel_solver/src/EquilibriumFlow.cpp

In the main, select one of the test networks (Braess, Toy, Chicago ...), or just select 'OSM-medium' if you want to conduct your own experiments. For Los Angeles, leave 'OSM_medium'.

Then to compile, you run 'make' in the root of the repo.

Depending on your system, rename the 'Makefile_yourSystem' in simply 'Makefile', and delete the other one. 

Run the experiments
-------------------------------

And then run the FW_algo_main.py in the traffic-estimation-wardrop-master.


Generating the input files for other cities
-------------------------------
The instructions for installing the dependencies are below.

FW_algo_main.py generates the inputs for the M.Steel solver. But FW_algo_main.py needs inputs corresponding to the city. 

The inputs it needs can be derived thanks to queries in PostGreSQL. 
One needs to download the TAZ data (shapefile format). For LA : use this link:  http://gisdata.scag.ca.gov/SitePages/GIS%20Library.aspx
Then load this shapefile file into PostGreSQL and perform the queries of postgres-queries.py (follow the directions and comments in postgres-queries.py if you are working in another city than Los Angeles, edit the file accordingly).
The output is going to be all the TAZs with their centroids. 

Then you'll need the Nodes and Links data of your network in a csv format. 
You can most likely find a shapefile format of your city thanks to OSM. Then I suggest you load these shapefiles into QGIS and export them as csv, following the instructions of this tutorial: http://www.gistutor.com/quantum-gis/19-beginner-quantum-gis-tutorials/59-how-to-create-a-shapefile-from-xy-data-using-qgis.html

Tip: Make sure to use the EPSG:4326 for Geo Coordinate Systems.

Output these csv (nodes and links) in the folder : Networks/data/CSV/ and change the names accordingly in the python files. 

Your last inputs will be the ODs. They are TAZ-based and for LA it is the file: CTPP_LA.csv


Installing QGIS (instructions for MAC OS):
-------------------------------
Installing GDAL on a Mac: http://www.gis.usu.edu/~chrisg/python/2009/docs/gdal_mac.pdf
Mac OS X frameworks for GDAL: http://www.kyngchaos.com/software:frameworks
Installing PostGIS: http://postgis.net/install
Mac OS X frameworks for PostgreSQL and PosGIS estension: http://www.kyngchaos.com/software/postgres


Importing shp, csv, json into PostGIS database
-------------------------------
Importing Shapefile into PostGIS: http://www.gistutor.com/postgresqlpostgis/4-beginner-postgresqlpostgis-tutorials/18-importing-shapefile-gis-data-into-postgresql.html

Converting json to csv: http://www.convertcsv.com/json-to-csv.htm

Importing csv to QGIS: http://www.qgistutorials.com/en/docs/importing_spreadsheets_csv.html

Creating a Shapefile from XY Data using QGIS (for L.A. choose EPSG:4326 for Geo Coordinate Systems): http://www.gistutor.com/quantum-gis/19-beginner-quantum-gis-tutorials/59-how-to-create-a-shapefile-from-xy-data-using-qgis.html

If 'Unable to convert data value to UTF-8' error when importing into PostGIS: http://gis.stackexchange.com/questions/39238/how-to-import-shp2pgsql
