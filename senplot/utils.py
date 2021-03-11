# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-11 15:04
@author: johannes

Some functions usable for nc files.
"""
import netCDF4


def load_data(fid):
    scene = netCDF4.Dataset(fid, 'r')
    return scene


def get_data(scene, key_data):
    data = scene.variables[key_data][:]
    return data.data[0]


def get_lat(scene, key_latitude='lat'):
    return scene.variables[key_latitude][:]


def get_lon(scene, key_longitude='lon'):
    return scene.variables[key_longitude][:]
