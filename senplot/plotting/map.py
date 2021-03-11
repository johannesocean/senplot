# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-11 13:53
@author: johannes
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


class PlotSatProd:
    """
    Well.. dated code..
    TODO: TIDY UP!
    """
    def __init__(self, data_mat=False,
                 lat_mat=False,
                 lon_mat=False,
                 cbar_label='',
                 cmap_step=2,
                 max_tick=20,
                 min_tick=0,
                 max_min_range=False,
                 set_maxmin_from_data=False,
                 use_frame=False,
                 map_frame=None,
                 delta_lat=False,
                 delta_lon=False,
                 resolution='l',
                 text=False,
                 show_fig=False,
                 save_fig=False,
                 fig_name=None,
                 fig_title=None,
                 save_dir='',
                 clear_fig=False,
                 p_color=False):

        data = data_mat
        self.lats = lat_mat
        self.lons = lon_mat

        self.delta_lat = delta_lat or 2
        self.delta_lon = delta_lon or 4

        self.resolution = resolution
        self.text = text
        self.save_dir = save_dir
        self.fig_title = fig_title or ''
        fig_name = fig_name or 'fig_name.png'
        self.cbar_label = cbar_label

        if max_min_range:
            self.min_tick = max_min_range[0]
            self.max_tick = max_min_range[1]
            self.cmap_step = self.max_tick / 10.
        else:
            if set_maxmin_from_data:
                self.min_tick = data[np.where(np.isfinite(data))].min()
                self.max_tick = data[np.where(np.isfinite(data))].max()
                self.cmap_step = self.max_tick / 10.
            else:
                self.cmap_step = cmap_step
                self.max_tick = max_tick
                self.min_tick = min_tick

        self.map_frame = map_frame or {'lat_min': 53.5, 'lat_max': 66., 'lon_min': 9., 'lon_max': 31.}
        self.use_frame = use_frame

        self._draw_map()

        self._draw_mesh(p_color, data)

        if show_fig:
            plt.show()
        if save_fig:
            self.save_figure(name=fig_name)
        if clear_fig:
            plt.close('all')

    def _draw_map(self):
        print('Drawing map...')
        self.map_figure = plt.figure()
        self.map_axes = self.map_figure.add_subplot(111)

        self.map = Basemap(projection='stere', boundinglat=53, lon_0=19, lat_0=60, resolution=self.resolution,
                           area_thresh=10.,
                           llcrnrlat=self.map_frame['lat_min'], urcrnrlat=self.map_frame['lat_max'],
                           llcrnrlon=self.map_frame['lon_min'], urcrnrlon=self.map_frame['lon_max'],
                           ax=self.map_axes)

        self.map.drawcoastlines(linewidth=0.25)
        self.map.drawcountries(linewidth=0.15)
        self.map.fillcontinents(color='black', lake_color='white')
        self.map.drawmapboundary(fill_color='white')
        self.map.drawparallels(np.arange(-81., 82., 2.), linewidth=0.5,
                               labels=[True, False, False, False])
        self.map.drawmeridians(np.arange(-177., 181., 4.), linewidth=0.5,
                               labels=[False, False, False, True])

    def _draw_mesh(self, p_color, data):
        print('Drawing mesh..')
        # Create 2D lat/lon arrays for Basemap
        # Transforms lat/lon into plotting coordinates for projection
        data[data <= 0] = np.nan
        x, y = self.map(self.lons, self.lats)
        color_map = 'viridis'  # plt.cm.jet
        # self.min_val = data[np.where(np.isfinite(data))].min()
        # self.max_val = data[np.where(np.isfinite(data))].max()
        extend = 'max'
        self.map_color_range = np.linspace(self.min_tick, self.max_tick,
                                           500, endpoint=False)
        self.map_tick_list = list(np.arange(self.min_tick, self.max_tick,
                                            self.cmap_step))

        if p_color:
            self.map_mesh = self.map_axes.pcolormesh(x, y, data,
                                                     cmap=color_map,
                                                     vmin=self.min_tick,
                                                     vmax=self.max_tick)
            self.map_mesh.cmap.set_under('white')

            cbar = plt.colorbar(self.map_mesh,
                                extend=extend,
                                orientation='vertical',
                                shrink=0.8)

            cbar.set_label(self.cbar_label)

        else:
            self.map_mesh = self.map_axes.contourf(x, y, data,
                                                   self.map_color_range,
                                                   cmap=color_map,
                                                   extend=extend,
                                                   )
            cbar = plt.colorbar(self.map_mesh, ticks=self.map_tick_list,
                                orientation='vertical', shrink=0.8)

            cbar.set_label(self.cbar_label)

        if self.text:
            self.add_text_box(self.map_axes, self.text)

        if hasattr(self, 'fig_title'):
            plt.title(self.fig_title, fontsize=10)

    @staticmethod
    def add_text_box(ax, textstr):
        # these are matplotlib.patch.Patch properties
        props = dict(facecolor='white', alpha=0.8)
        # 0.565, 0.966
        # place a text box in upper left in axes coords
        ax.text(0.040, 0.966, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='left',
                bbox=props,
                zorder=21)

    @staticmethod
    def save_figure(name='test_plot.png'):
        plt.tight_layout()
        plt.savefig(name, bbox_inches='tight', dpi=100)
