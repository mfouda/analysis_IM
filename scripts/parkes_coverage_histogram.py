import fnmatch
import os
import numpy as np
import pyfits
import matplotlib.pyplot as plt
from pylab import *

def find_pattern(pattern,root_dir):
    matches = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))

    return matches

#matches = find_pattern("*west2*.sdfits","/mnt/raid-project/gmrt/raid-pen/pen/Parkes/2dF/DATA/p641/sdfits/rawdata/")
#matches = open('sorted_datalist_2012_ycf.txt', 'r').read().splitlines()
matches = open('final_datalist.txt', 'r').read().splitlines()

def fix(list):
    wh_wrap = (list>180)
    list[wh_wrap] = list[wh_wrap] - 360
    return list

def ra_max(list):
    ra_max_list = []
    for file in list:
        hdulist = pyfits.open(file)
        hdu_data = hdulist[1]
        ra_vec = fix(hdu_data.data['CRVAL3'])
        ra_max_file = np.max(ra_vec)
        ra_max_list.append(ra_max_file)
    max_ra = max(ra_max_list)
    return max_ra

def ra_min(list):
    ra_min_list = []
    for file in list:
        #print file
        hdulist = pyfits.open(file)
        hdu_data = hdulist[1]
        ra_vec = fix(hdu_data.data['CRVAL3'])
        ra_min_file = np.min(ra_vec)
        ra_min_list.append(ra_min_file)
    min_ra = min(ra_min_list)
    return min_ra

def dec_max(list):
    dec_max_list = []
    for file in list:
        hdulist = pyfits.open(file)
        hdu_data = hdulist[1]
        dec_vec = hdu_data.data['CRVAL4']
        dec_max_file = np.max(dec_vec)
        dec_max_list.append(dec_max_file)
    max_dec = max(dec_max_list)
    return max_dec

def dec_min(list):
    dec_min_list = []
    for file in list:
        hdulist = pyfits.open(file)
        hdu_data = hdulist[1]
        dec_vec = hdu_data.data['CRVAL4']
        dec_min_file = np.min(dec_vec)
        dec_min_list.append(dec_min_file)
    min_dec = min(dec_min_list)
    return min_dec

def saveplot(hist, extent, j):
    currentplot=plt.imshow(hist, vmax=190, vmin=0, extent=extent, interpolation='nearest')
    plt.colorbar()
    #plt.savefig('/cita/h/home-2/anderson/anderson/parkes_analysis_IM/parkes_2012_movie_yc/' + '{0:03}'.format(j), bbox_inches=0)
    plt.savefig('/cita/h/home-2/anderson/anderson/parkes_analysis_IM/parkes_nodriftcal_movie/' + '{0:03}'.format(j), bbox_inches=0)
    plt.close()

hitmap = np.zeros((50,200))
ran=ra_min(matches)
rax=ra_max(matches)
decn=dec_min(matches)
decx=dec_max(matches)
i=1
#saveplot(hitmap, [-20,20,-24,-34],1)
for file in matches:
    #print file
    hdulist = pyfits.open(file)
    hdu_data = hdulist[1]
    ra_vec = fix(hdu_data.data['CRVAL3'])
    dec_vec = hdu_data.data['CRVAL4']
    (skycov, dec_edge, ra_edge) = np.histogram2d(dec_vec, ra_vec,
                                                 range=[[decn,decx],[ran,rax]],                                                  bins=hitmap.shape)
    hitmap += skycov
    extent=[ra_edge[0], ra_edge[-1], dec_edge[0], dec_edge[-1]]
    saveplot(hitmap, extent, i)
    i += 1

#extent=[ra_edge[0], ra_edge[-1], dec_edge[0], dec_edge[-1]]
#plt.imshow(hitmap, vmax=50, vmin=0, extent=extent, interpolation='nearest')
#plt.imshow(hitmap, extent=extent, interpolation='nearest')
#plt.colorbar()
#plt.show()
#print hitmap
