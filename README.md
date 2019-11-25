# SPOLVERRO
### A method for analyzing single-spot analysis referenced to spectral imaging and its application in the diagnostic of Cultural Heritage.

**SPOLVERRO** (like [spolvero](https://it.wikipedia.org/wiki/Spolvero) but with two 'r') is a set of tools used for analyzing **S**pectral data with **P**CA **O**n pictorial **L**ayers represented as **V**ectors **E**xtracted from **R**asters images **R**eferenced **O**nsite.

In this repository you can find some utilities and tutorial for analyzing data acquired with single-spot techniques referenced over spectral imaging cubes.

![Alt text](images/visualabstract.jpg?raw=true "Graphic representation of the method proposed")

This work was specifically design for applications in diagnostic of Cultural Heritage, here we present what concern the implementation of the method using open-source Python libraries.

If you are new to Python the easiest way to get started is to install a Python distribution such as [Anaconda](https://www.anaconda.com/).

In the example folder an interactive Jupyter notebook shows how the idea is implemented.
The functions shown in the notebook can be also run installing the Python module SPOLVERRO.
This can be done using:

```
pip install git+https://github.com/giacomomarchioro/spolverro
```

## Basic usage of the module
This basic example shows the functionality over the test data.

  ```python
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
  ```

### Test data
The test data are portion of a data set collected during Hyperion project on a painting by Vittore Carpaccio (in alphabetical order) by Nicole De Manincor, Enrico Fiorin and Marco Raffaelli, and can not be published without consent.
