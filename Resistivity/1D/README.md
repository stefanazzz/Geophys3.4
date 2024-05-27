# 1D resistivity inversion
- stand alone code "schlum_example.ipynb" based on pygimli 
- general electrode geometry ABMN (P1 P2 C1 C2), only requirement is AM <-> BN symmetry
 
How to produce a soil resistivity model:

1) Write data in file

put all your data in a csv file (save from excel microsoft format csv and Unicode UTF-8.
The format of the file shold be comma separated values with 6 columns like this:

MN/2 (m), AB/2 (m), R1 (ohms), R2 (ohms), R3 (ohms), R4 (ohms)
0.5,      1,        298,       298,       298,       298
0.5,      1.25,     195.3,     195.2,     195,       195.2
etc... etc...

an example file of input is provided (input_example.csv).

3) Upload files on the server:

 - the csv data file that you have compiled

4) Run the notebook

 - run the notebook cells sequentially from top to bottom
 - make sure you replace 'input_example.csv' by the name of your own data file 
 - make a hypothesis on the number of layers. Start with 3 then add more to see what minimum number of layers fit the data
 - the final cell in the notebook creates a resistivity model from the data, by performing an inverse problem
