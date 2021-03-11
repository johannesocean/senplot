# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-11 13:52
@author: johannes
"""
# import os
# os.environ['PROJ_LIB'] = '...\\envs\\__ENV_NAME__\\Library\\share\\proj'

import numpy as np
from datetime import datetime
from satpy import Scene, find_files_and_readers
from senplot.plotting.map import PlotSatProd


if __name__ == '__main__':
    sen3_data_l2 = 'C:/Temp/Satellit/sentinel_data'

    # datetime(YEAR, MOMNTH, DAY, HOUR, MINUTE)
    filenames = find_files_and_readers(
        start_time=datetime(2021, 2, 13, 7, 10),
        end_time=datetime(2021, 2, 13, 12, 50),
        base_dir=sen3_data_l2,
        reader='olci_l2',
        sensor='olci',
    )

    """ Create Scene object """
    scn = Scene(filenames=filenames)

    """ Load selected datasets 
        Available OLCI Level 2 datasets are:
            'chl_nn.nc','chl_oc4me.nc',
            'iop_nn.nc','iwv.nc','par.nc','trsp.nc','tsm_nn.nc','w_aer.nc',
            'Oa01_reflectance.nc','Oa02_reflectance.nc','Oa03_reflectance.nc','Oa04_reflectance.nc','Oa05_reflectance.nc','Oa06_reflectance.nc','Oa07_reflectance.nc','Oa08_reflectance.nc','Oa09_reflectance.nc','Oa10_reflectance.nc','Oa11_reflectance.nc','Oa12_reflectance.nc','Oa16_reflectance.nc','Oa17_reflectance.nc','Oa18_reflectance.nc','Oa21_reflectance.nc',
            'wqsf.nc'
    """
    datasets = [
        'chl_nn',
        # 'chl_oc4me',
    ]
    scn.load(datasets)

    """ Resample data to grid (projecting) """
    area_spec = 'baws'  # 1000 m resolution grid over the Baltic Sea incl. Kattegatt and Skagerrak
    # scn = scn.resample(area_spec, radius_of_influence=300)

    """ Chlorophyll data are stored as logarithmic values. Convert to real values: """
    scn['chl_nn'] = np.power(10, scn['chl_nn'])

    """ Simple plot """
    scn['chl_nn'].plot()

    """ Save as geotiff?.. and possibly drag into QGIS? """
    # scn.save_dataset(
    #     'chl_nn',
    #     filename='/__PATH_TO_FOLDER__/__FILENAME__.tiff',
    #     writer='geotiff',
    #     dtype=np.float32,
    #     enhance=False,
    # )

    """ Advanced map plot. PlotSatProd needs to be cleaned up!!! 
        See PlotSatProd.__init__(...) for more options """

    # lons, lats = scn['chl_nn'].area.get_lonlats()
    # PlotSatProd(
    #     data_mat=scn['chl_nn'].data,
    #     lat_mat=lats,
    #     lon_mat=lons,
    #     cbar_label='Chl µg/l',
    #     cmap_step=2,
    #     max_tick=10,
    #     min_tick=0,
    #     resolution='i',
    #     map_frame={'lat_min': 54., 'lat_max': 60., 'lon_min': 5., 'lon_max': 14.},
    #     p_color=True,
    #     show_fig=True,
    #     save_fig=True,
    #     fig_title='OLCI Level 2 - chl_nn - 2021-02-13',
    #     fig_name='chl_test_plot.png',
    # )
