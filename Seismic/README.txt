Use of the code:
----------------
- upload the dat or DAT files
  (an example data set is already in 'ExampleData' with the picking done).
- run Picking_3.x.ipynb
    - first modify interactive widgets if needed to set:
        - file name, path
        - geophone spacing 
        - if a geophone has been moved and where for this shot
        etc
    - second, pick with right mouse click
    - third, run cell that saves results in new file
    - repeat for each shot gather file
- run Seismic_Inversion_3.4x.ipynb
    - first modify text in interactive widgets if needed to set:
        - path to files
        - filenames
        - avg error
    - then run the cells to perform inversion and plotting
    - modify the parameters of inversion if needed

Requirements:
------------
- python3 environment with pygimli, pandas, ipywidgets (in addition to several python installed by default, numpy, matplotlib, etc) 
- files:
    - Picking_3.4.ipynb
    - Seismic_inversion_3.4.ipynb
    - dict.yml (initial dictionary file with default parameters for the widgets. This is automatically updted when valueds are changed)
    - Init_Picking_3.4.py (various functions defined that are used in the Picking_3 code)
    - Init_Seismic_Inversion_3.4.py (various functions defined that are used in the Picking_3 code)