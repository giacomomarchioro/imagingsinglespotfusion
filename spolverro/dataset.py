#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:57:41 2019

@author: giacomo
"""


from __future__ import print_function
import rasterio # for loading the rasters
from rasterio import plot as rasterplot
import shapefile # for loading the XRF shapefile
import matplotlib.pyplot as plt
import numpy as np
from .subdataset import subdataset

class  dataset:
       
    def __init__(self,raster_path,shapefile_path):
        self.rasterpath = raster_path
        self.shpfilepath = shapefile_path
        self.raster = subdataset(rasterio.open(raster_path))
        self.shapefile = subdataset(shapefile.Reader(shapefile_path))
        self.fused_dataset = subdataset()
        self.extracted_points = None
        
    def extract_plot(self,r=1,g=2,b=3,ROI_side=5,show=True):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        reflectance_perpoint_l = []
        reflectance_stdv = []
        ids = []
        extracted_xrf = []
        resx, resy = self.raster.obj.res
        def area_ex(coor):
            '''
            This function create a a list of coordinates [x,y]
            within a number of pixel extent around the initial
            value.
            '''
            ls_coor = []
            half_lim = int(ROI_side/2)
            for i in range(-half_lim,half_lim):
                for j in range(-half_lim,half_lim):
                    # we multiply the number for the x, y pixel size 
                    ls_coor.append([(coor[0] + i)*resx,(coor[1] + j)*resy])
            return ls_coor
          
        for xrfpoint,record in zip(self.shapefile.obj.shapes(),
                                   self.shapefile.obj.records()):
            x,y = xrfpoint.points[0]
            sampling = area_ex([x, y])
            for i in sampling:
                x,y = i
                ax.scatter(x,y,color='w',alpha=0.5)
            # Now we sample the multi-spectral cube
            try:
                generators = self.raster.obj.sample(area_ex([x, y]))
                extracted_points = [i for i in generators]
                reflectance_perpoint_l.append(np.mean(np.array(extracted_points),axis = 0))
                reflectance_stdv.append(np.std(extracted_points,axis = 1))
                ids.append(record[0])
                extracted_xrf.append(record)
            except ValueError:
                TypeError('Sampling out of bound')
 
        self.raster.datamatrix = np.array(reflectance_perpoint_l)
        self.raster.ids = ids
        self.shapefile.datamatrix = np.array(extracted_xrf)
        self.shapefile.ids = ids
        self.extracted_points = extracted_points
        if show:
            rasterplot.show((self.raster.obj,(r,g,b)),zorder=0,ax=ax)
            plt.show()
            
    def fuse_data(self):
        
        self.fused_dataset.datamatrix = np.hstack([self.shapefile.datamatrix,
                                                      self.raster.datamatrix])
        self.fused_dataset.ids = self.raster.ids
        try:
            self.fused_dataset.variables_name = self.shapefile.variables_name + self.raster.variables_name
        except TypeError:
            print("Variables name not available for both dataset!")

            
    def extract_variablesnames_fromShapefile(self):
        variables_name = [i[0] for i in self.shapefile.obj.fields[1:]]
        self.shapefile.variables_name = variables_name
        
        




    
        