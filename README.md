BaySim
======

DataBay hackathon project (Aug 1-3, 2014)


Derived from a CS class on teaching programming in python, this
simcity style game adds a realistic map of the Cheseapeake Bay and
allows you to study the interplay of water levels, pollution and a
crab population as a measure of the health of the ecosystem.

Running BaySim
--------------

BaySim is written in python, and does currently not need any special
libraries, though it uses tk for display and the cells are hardcoded
in size (8 pixels currently)

The code should simply by either "import ui" from the python prompt, 
or by issuing the command 

   python ui.py 

or simply execute the BaySim script from the shell:

   BaySim


Input Data
----------

The current input elevation map is a simple ascii table with 3
columns: X, Y, ELEV, although currently X and Y are ignored and 
the data must be entered row by row, starting at the bottom.

This ascii table has been created by a shell script `convert_png2elev`
from screendump type PNG from ArcGIS. Because of the limited dynamic
range (0-255) of PNG's, we took two PGNs to represent the land, the
first 100m and the 100-300m.  The depth of the bay came from
bathascopy. The script scales and combines the three, and creates that
ascii file for input to BaySim. There are no doubt better ways to get
this table, but with the limited time/resources this is what we wind up
producing.
