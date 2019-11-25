#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:14:22 2019

@author: giacomo
"""

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from mpl_toolkits.mplot3d import Axes3D  

class subdataset:
    def __init__(self,datasetobj=None):
        self.path = None
        self.variables_name = None
        self.ids = None
        self.obj = datasetobj
        self.datamatrix = None
        self.scaled_datametrix = None
    
    def select_columns(self,start_column = None, end_column = None):
        self.variables_name = self.variables_name[start_column:end_column]
        sd = self.datamatrix[:,start_column:end_column]
        self.datamatrix = sd.astype(np.float)
        if self.scaled_datametrix != None:
             d = self.scaled_datametrix[:,start_column:end_column]
             self.scaled_datametrix = d.astype(np.float)
             
    def plotPCA(self,
                n_components=3,
                x_component=0,
                y_component=1,
                scaling=False,
                colors = None,
                labels_dict = None,
                show=True):
        """
        This function is used to plot the PCA.
        It plots the score plot and the loading plot of two componets. 
        """

        dict_ord = {0:'First',1:'Second',2:'Third',3:'Forth'}
        # compute the trasform
        sklearn_pca = sklearnPCA(n_components=n_components)
        if scaling: 
            ds = StandardScaler().fit_transform(self.datamatrix)
        else:
            ds = self.datamatrix
        sklearn_transf = sklearn_pca.fit_transform(ds)
        c1 = sklearn_pca.explained_variance_ratio_[x_component]
        c2 = sklearn_pca.explained_variance_ratio_[y_component]
        c1exp_variance= round(c1*100,2)
        c2exp_variance= round(c2*100,2)
        
        # SCORE PLOT
        
        figc = plt.figure()
        axc = figc.add_subplot(111)
        axc.set_xlabel('%s component (%s %%)' %(dict_ord[x_component],
                       c1exp_variance))
        axc.set_ylabel('%s component (%s %%)' %(dict_ord[y_component],
                       c2exp_variance))
        xmin = np.min(sklearn_transf[:,x_component])
        xmax = np.max(sklearn_transf[:,x_component])
        ymin = np.min(sklearn_transf[:,y_component])
        ymax = np.max(sklearn_transf[:,y_component])
        axc.set_xlim(xmin+xmin*0.1,xmax+xmax*0.1)
        axc.set_ylim(ymin+ymin*0.1,ymax+ymax*0.1)
        
            
        if colors is None:
            for coord, label in zip(sklearn_transf[:,[x_component,
                                                      y_component]],
                                    self.ids):
                color = 'k'
                if labels_dict is not None:
                    label_txt,color = labels_dict[label]
                    label = "%s-%s" %(label,label_txt)
                axc.text(coord[0],
                         coord[1],
                         label,
                         fontsize=13,
                         ha='center',
                         va='center',
                         color = color,
                         clip_on=True)
        else:
            for coord, label,color in zip(sklearn_transf[:,[x_component,
                                                            y_component]],
                                    self.ids,colors):
                color2 = 'white'
                if labels_dict is not None:
                    label_txt,color2 = labels_dict[label]
                    label = "%s-%s" %(label,label_txt)
                axc.text(coord[0],coord[1],label,fontsize=13,
                         ha='center',
                         va='center',
                         clip_on=True,
                         color=color2)
                axc.scatter(coord[0],coord[1],marker="o",color=color,s=400)
        
        
        axc.grid(True)
        axc.set_title('Score Plot (Correlation Matrix)')
        # LOADING PLOT
        loadings = sklearn_pca.components_
        figL = plt.figure()
        ax4 = figL.add_subplot(111)
        ax4.plot(loadings[x_component],'x',
                 label="Loadings %s component" %(dict_ord[x_component]),
                 markersize=12)
        ax4.plot(loadings[y_component],'x',
                 label="Loadings %s component" %(dict_ord[y_component]),
                 markersize=12)
        ax4.xaxis.set_ticks(range(0,ds.shape[1]+1))
        if self.variables_name is not None:
            ax4.set_xticklabels(self.variables_name)
            
        ax4.set_title("Loading plot")
        ax4.set_xlabel(" PC Variables")
        ax4.set_ylabel("Arbitrary")
        ax4.legend()
        ax4.grid()
        plt.setp( ax4.xaxis.get_majorticklabels(), rotation=70 )
        figL.tight_layout()
        self.scaled_datametrix = ds
        if show:
            plt.show()
        



    def plotPCA3D(self,n_components=3,
                x_component=0,
                y_component=1,
                z_component=2,
                legend_elements=None,
                scaling=False,
                labels_dict = None,
                show=True):
        """
        This function is used to plot the PCA.
        It plots the score plot and the loading plot of two componets. 
        """
        dict_ord = {0:'First',1:'Second',2:'Third',3:'Forth'}
        # compute the trasform
        sklearn_pca = sklearnPCA(n_components=n_components)
        if scaling: 
            ds = StandardScaler().fit_transform(self.datamatrix)
        else:
            ds = self.datamatrix
            
        sklearn_transf = sklearn_pca.fit_transform(ds)
        c1 = sklearn_pca.explained_variance_ratio_[x_component]
        c2 = sklearn_pca.explained_variance_ratio_[y_component]
        c3 = sklearn_pca.explained_variance_ratio_[z_component]
        c1exp_variance= round(c1*100,2)
        c2exp_variance= round(c2*100,2)
        c3exp_variance= round(c3*100,2)
        #  3D SCORE PLOT
        figc = plt.figure()
        axc = figc.add_subplot(111, projection='3d')
        axc.set_xlabel('%s component \n (%s %%)' %(dict_ord[x_component],
                       c1exp_variance))
        axc.set_ylabel('%s component \n (%s %%)' %(dict_ord[y_component],
                       c2exp_variance))
        axc.set_zlabel('%s component \n (%s %%)' %(dict_ord[z_component],
                       c3exp_variance))
        xmin = np.min(sklearn_transf[:,x_component])
        xmax = np.max(sklearn_transf[:,x_component])
        ymin = np.min(sklearn_transf[:,y_component])
        ymax = np.max(sklearn_transf[:,y_component])
        zmin = np.min(sklearn_transf[:,z_component])
        zmax = np.max(sklearn_transf[:,z_component])
        # for depth shading
        x_range = xmax - xmin
        y_range = ymax - ymin
        axc.set_xlim(xmin+xmin*0.1,xmax+xmax*0.1)
        axc.set_ylim(ymin+ymin*0.1,ymax+ymax*0.1)
        axc.set_zlim(zmin+zmin*0.1,zmax+zmax*0.1)
        axes = figc.gca(projection='3d')
        axes.xaxis.labelpad=30
        axes.yaxis.labelpad=30
        axes.zaxis.labelpad=30
        
            
        for coord, label in zip(sklearn_transf[:,[x_component,
                                                  y_component,
                                                  z_component]],
                                self.ids):
            
                cxalpha = 0.4*((coord[0]-xmin)/x_range)
                cyalpha = 0.4 - 0.4*((coord[1]-ymin)/y_range)
                alpha = cxalpha+cyalpha+0.2
                if labels_dict != None:
                    marker,color= labels_dict[label]
                else: 
                    marker,color = 'v','r'
                axc.scatter(coord[0],coord[1],coord[2],
                            marker=marker,
                            color=color,
                            depthshade=True,
                            s=200*alpha,
                            alpha=alpha)
        
        if legend_elements != None:
          axc.legend(handles=legend_elements)
          axc.legend()
        axc.grid(True)
        axc.set_title('Score Plot (Correlation Matrix)')
        axc.xaxis._axinfo['label']['space_factor'] = 2.8
        axc.dist = 13
        axes = figc.gca(projection='3d')
        axes.xaxis.labelpad=20
        axes.yaxis.labelpad=20
        axes.zaxis.labelpad=20
        # LOADING PLOT
        loadings = sklearn_pca.components_
        figL = plt.figure()
        ax4 = figL.add_subplot(111)
        ax4.plot(loadings[x_component],'x',
                 label="Loadings %s component" %(dict_ord[x_component]),
                 markersize=12)
        ax4.plot(loadings[y_component],'x',
                 label="Loadings %s component" %(dict_ord[y_component]),
                 markersize=12)
        ax4.plot(loadings[z_component],'x', 
                 label="Loadings %s component" %(dict_ord[y_component]),
                 markersize=12)
        ax4.xaxis.set_ticks(range(0,ds.shape[1]+1))
        if self.variables_name is not None:
            ax4.set_xticklabels(self.variables_name)
        ax4.set_title("Loading plot",linespacing=3.1)
        ax4.set_xlabel(" PC Variables",linespacing=3.1)
        ax4.set_ylabel("Arbitrary",linespacing=3.1)
        ax4.legend()
        ax4.grid()
        plt.setp( ax4.xaxis.get_majorticklabels(), rotation=70 )
        figL.tight_layout()
        self.scaled_datametrix = ds
        if show:
            plt.show()
            
    def plot_spectrum(self,index,norm=False):
        '''
        Plot the spectrum corresponding to a given sample index.
        '''
        figs = plt.figure()
        ax5 = figs.add_subplot(111)
        if norm:
            spectrum = self.datamatrix[index-1,:]/2.55
            ax5.set_ylabel("Reflectance (%)")
            ax5.set_ylim(0,100)
        else:
            spectrum = self.datamatrix[index-1,:]
            ax5.set_ylabel("Counts")
        ax5.plot(spectrum,'x',markersize=12)
        ax5.xaxis.set_ticks(range(0,self.datamatrix.shape[1]+1))
        if self.variables_name is not None:
            ax5.set_xticklabels(self.variables_name)
        ax5.set_title("Spectrum %s" %(index))
        
        
        ax5.legend()
        ax5.grid()
        plt.setp(ax5.xaxis.get_majorticklabels(), rotation=70 )
        figs.tight_layout()