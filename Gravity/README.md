# Build 2D model and estimate gravity anomaly
- Build model by either 
  - use of interactive graphic
  - or by defining arrays of (x,y) polygon vertexes
- Compute gravity anomaly using **pygimli**
- Compare to field data
## Main code is
  - ModeMeshGravity_2024.ipynb
## Requires
- companion file InitMdodelMechGravity_2024.ipynb
- example files data_example2.csv, m1.tmp, m2.tmp, m3.tmp
- modules/environment listed in root folder
## Bouguer or direct
- Use topography to direct model data or reference horizon for Bouguer corrected data
