import numpy as np
import xarray as xr
from scipy.ndimage import median_filter, uniform_filter, generic_filter

from satpy import Scene, find_files_and_readers
from datetime import datetime
import matplotlib.pyplot as plt
from pyresample import load_area
import warnings
warnings.filterwarnings('ignore')


def get_median_filter(data, size=3):
    """Apply median filter on data."""
    return xr.apply_ufunc(
        median_filter, data,
        input_core_dims=[['y', 'x']],
        output_core_dims=[['y', 'x']],
        vectorize=True,
        dask='parallelized',
        dask_gufunc_kwargs=dict(allow_rechunk=True),
        output_dtypes=[data.dtype],
        kwargs={'size': size}
    )


def get_mean_filter(data, size=3):
    """Apply mean filter on data, handling NaN values."""

    def within_one_std(_data):
        center_value = _data[size // 2]
        if np.isnan(center_value):
            return np.nan
        mean = np.nanmean(_data)
        std = np.nanstd(_data)
        mask = np.logical_and(_data >= mean - std, _data <= mean + std)
        filtered_data = np.where(mask, _data, np.nan)
        return np.nanmean(filtered_data)

    return xr.apply_ufunc(
        generic_filter, data,
        input_core_dims=[['y', 'x']],
        output_core_dims=[['y', 'x']],
        vectorize=True,
        dask='parallelized',
        dask_gufunc_kwargs=dict(allow_rechunk=True),
        output_dtypes=[data.dtype],
        kwargs={
            # 'function': np.nanmean,
            'function': within_one_std,
            'size': size,
            'mode': 'constant',
            'cval': np.NaN
        }
    )


if __name__ == '__main__':
    sen3_data_l2 = r'D:\temp\Satellit\sentinel_data'

    filenames = find_files_and_readers(
        start_time=datetime(2022, 6, 30, 7, 20),
        end_time=datetime(2022, 6, 30, 11, 25),
        base_dir=sen3_data_l2,
        reader='olci_l2',
        sensor='olci',
    )

    scn = Scene(filenames=filenames)

    datasets = ['chl_nn', 'wqsf']
    scn.load(datasets)
    scn['chl_nn'] = np.power(10, scn['chl_nn'])
    chunk = scn['chl_nn'][2250:2450, 400:600]
    # scn['chl_nn'].plot()
    # scn.save_dataset('chl_nn', dtype=np.float32, enhance=False)

    # Applicera en 3x3 medianfilter på rasterdata
    filtered_median_data_3x3 = get_median_filter(chunk, size=3)
    filtered_median_data_5x5 = get_median_filter(chunk, size=5)

    filtered_mean_data_3x3 = get_mean_filter(chunk, size=3)
    filtered_mean_data_5x5 = get_mean_filter(chunk, size=5)

    data_chunks = [chunk,
                   # filtered_median_data_3x3, filtered_median_data_5x5,
                   filtered_mean_data_3x3, filtered_mean_data_5x5]
    fig, axes = plt.subplots(len(data_chunks), 1, figsize=(8, 16))

    for i, dset in enumerate(data_chunks):
        im = axes[i].imshow(dset, vmin=0, vmax=10, cmap='jet')
        axes[i].set_title(f'Subplot - Row {i + 1}')

    cbar = fig.colorbar(im, ax=axes.ravel().tolist())
    # plt.clim(0, 10)
