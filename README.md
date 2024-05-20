jupyter lab:

https://mybinder.org/v2/gh/stefanazzz/Geophys3.4/main

classic notebook:

https://mybinder.org/v2/gh/stefanazzz/Geophys3.4/main?filepath=ERT2D_dat_res_3.4.ipynb

Testbench for geophysical imaging codes to use online interactively.
Uses pygimli, obspy, pandas, shapely, etc
-----------------------------------------------------------
aims:
- workable on jupyterlab / mybinder
- minimum possible environment footprint
- replace %matplotlib noteobbk by %matplotlib widget
- create sharable online version and backup for Durham class
creation of enviroment with conda:
   conda create -n geo05 -c gimli -c conda-forge "pygimli>=1.5.0"
   conda activate geo05
   pip install jupyterlab
   pip install pandas
   pip install ipympl
   conda install obspy
   pip install shapely
environment.yml file for MYBINDER:
channels:
  - conda-forge
  - gimli
  - defaults
dependencies:
  - python=3.8
  - pygimli>=1.1.0
  - obspy
  - ipympl
  - pandas
  - shapely
