# SenPlot
Basically a place to gather example scripts to plot Sentinel 3 - data (OLCI and SLSTR) using the satpy library.

See senplot/senplot/examples/

Install dependencies
--------

See the [installation docs](https://satpy.readthedocs.io/en/stable/install.html)
for all details regarding Satpy. 
SenPlot depends on the following packages:

- ``satpy``
- ``numpy``
- ``matplotlib``
- ``basemap``
- ``basemap-data-hires``


If you are running python in a conda environment try:```conda install -c conda-forge --file requirements.txt``` 
(often a better option). Otherwise you could try:```pip install -r requirements.txt```

Example Chlorophyll
--------
![Example Chlorophyll](senplot/etc/chl_nn_test_plot.png)

Example Sea Surface Temperature
--------
![Example SST](senplot/etc/sst_test_plot.png)