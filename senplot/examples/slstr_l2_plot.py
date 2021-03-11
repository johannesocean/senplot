# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-11 16:08
@author: johannes
"""
# import os
# os.environ['PROJ_LIB'] = '/_PYTHON_INSTALLATION_PATH_/Library/share/proj'

import numpy as np
from datetime import datetime
from satpy import Scene, find_files_and_readers
from senplot.plotting.map import PlotSatProd


if __name__ == '__main__':
    sen3_data_l2 = 'C:/Temp/Satellit/sentinel_data'

    # datetime(YEAR, MOMNTH, DAY, HOUR, MINUTE)
    filenames = find_files_and_readers(
        start_time=datetime(2020, 6, 1, 7, 10),
        end_time=datetime(2020, 6, 1, 12, 50),
        base_dir=sen3_data_l2,
        reader='slstr_l2',
        sensor='slstr_l2',
    )

    """ Create Scene object """
    scn = Scene(filenames=filenames)

    """ Load selected datasets 
        Available SLSTR Level 2 datasets are: 
            'sea_surface_temperature', 'longitude', 'latitude'
    """
    datasets = ['sea_surface_temperature', 'longitude', 'latitude']
    scn.load(datasets)

    """ Resample data to grid (projecting) """
    # area_spec = 'baws'  # 1000 m resolution grid over the Baltic Sea incl. Kattegatt and Skagerrak
    # scn = scn.resample(area_spec, radius_of_influence=1000)

    """ Temperature data are stored as Kelvin degrees. Convert to Celsius values: """
    scn['sea_surface_temperature'] = scn['sea_surface_temperature'] - 273.15

    """ If we don´t have a proper mask to exclude bad data (usually beneth and around clouds), we can try to exclude 
    based on unlikely values. 
    Example below: It´s summertime and no obvious upwelling events, we exclude all temperature values < 8 degrees C. """
    scn['sea_surface_temperature'].data = np.where(
        scn['sea_surface_temperature'].data < 8,
        np.nan,
        scn['sea_surface_temperature'].data
    )

    """ Simple plot """
    # scn['sea_surface_temperature'].plot()

    """ Save as geotiff?.. and possibly drag into QGIS? """
    # scn.save_dataset(
    #     'sea_surface_temperature',
    #     filename='/__PATH_TO_FOLDER__/__FILENAME__.tiff',
    #     writer='geotiff',
    #     dtype=np.float32,
    #     enhance=False,
    # )

    """ Advanced map plot. PlotSatProd needs to be cleaned up!!! 
        See PlotSatProd.__init__(...) for more options """
    PlotSatProd(
        data_mat=scn['sea_surface_temperature'].data,
        lat_mat=scn['latitude'].data,
        lon_mat=scn['longitude'].data,
        cbar_label='Temperature $^{o}$C',
        cmap_step=2,
        max_tick=20,
        min_tick=0,
        resolution='i',
        map_frame={'lat_min': 53.5, 'lat_max': 61., 'lon_min': 9., 'lon_max': 23.},
        p_color=True,
        show_fig=True,
        save_fig=True,
        fig_title='SLSTR Level 2 - SST - 2020-06-01',
        fig_name='sst_test_plot.png',
    )
