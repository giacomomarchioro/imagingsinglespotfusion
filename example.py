# coding: utf-8
from spolverro import dataset
# We load the datasets
g = dataset(raster_path = "./examples/testdata/testdata.tif",
            shapefile_path = "./examples/testdata/xrfdata.shp")
# We extract the value and plot the position
g.extract_plot(r=9, g=6, b=3)
# We extract teh variables names
g.extract_variablesnames_fromShapefile()
g.shapefile.variables_name
# We can see that the first and the last two columns are not spectroscopy data
# but ID , attribution and notes, so we select only the other columns
g.shapefile.select_columns(start_column=1,end_column=-2)
# We can compute the PCA only on the shapefile, and display the first two 
# components with index 0 and 1.
g.shapefile.plotPCA(n_components=3,x_component=0,y_component=1)
# We can do the same for the raster dataset
# We add manually the variable to the raster dataset
g.raster.variables_name = ["395 nm", "415 nm", "455 nm", "485 nm", "510 nm", 
 "530 nm", "550 nm", "570 nm", "590 nm", "610 nm", "630 nm", "650 nm", "675 nm", 
 "705 nm", "735 nm", "765 nm", "750 nm", "850 nm", "950 nm", "1050 nm", 
 "1230 nm", "1292 nm", "1400 nm", "1500 nm", "1600 nm", "1705 nm",  "1830 nm",
 "1940 nm", "2100 nm", "2200 nm", "2345 nm", "2550 nm", ]
# This time we plot the PCA in 3D
g.raster.plotPCA3D(n_components=3,x_component=0,y_component=1,z_component=2)
# We fuse the results of the raster and the shape file
g.fuse_data()
# Now we can compute the PCA on the fused datset we standardize the whole 
# dataset using scaling = True
g.fused_dataset.plotPCA3D(scaling=True)

