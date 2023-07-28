# PiezoProject
Repository for Python code relating to the University of Michigan piezo positioner test stand. 

Last updated: 07/28/2023.

User manual: https://docs.google.com/document/d/1pZa10o1XOrTdqq4Kcskxd7lwNJab01iaerL3jmyTxpM

Required Python packages (that you would need to install):

pyvisa: https://anaconda.org/conda-forge/pyvisa

PySimpleGUI: https://anaconda.org/conda-forge/pysimplegui

pypylon: https://pypi.org/project/pypylon/

# Files
`AutoDriftTest.ipynb`: notebook for looking at drift and angular alignment of axis

`GetConversion.py`: can be used to measure the conversion factor in a bright photo

`LiveVid.py`: show a live image of the spine tip 

`LongTermTest.py`: used for looking at distance moved for given parameters over hours and hours, also the outline for calibrating micro moves

`MakeXYGrid.ipynb`: notebook showing how the XY grid is generated 

`PiezoGUI.py`: user interface for extensive testing

`PlotAutoDriftTest.ipynb`: used to plot a drift test 

`PlotVelocityTest.ipynb`: used to plot velocity tests

`PlotXYTestWinCond.ipynb`: used to plot XY test with the win condition or the grid test

`PlotXYTest.ipynb`: used to plot a basic XY test

`PlotXYTestWinCond.ipynb`: used to plot XY test with the win condition or the grid test

`StillErrorOverRange.ipynb`: used to test the detection error at multiple points across the spine's range

`TinyMoveTesting.ipynb`: for testing the smaller moves

`TinyMovements.py`: the medium sized move, calibrated based on micro move but runs for double the time to do slightly larger distances

`WaveformTesting-Copy1.ipynb`: more waveform testing code 

`WaveformTesting.ipynb`: older waveform testing code 

`Waveform_autotest.py`: function for easy repeated testing of movement from waveform

`config_constants.py`: contains all numerical values that describe the setup and calibrated moves 

`datacollectsoftware-CopyRS.ipynb`: new way to detect position with minimal error

`log.csv`: tracks the tests performed

`piezolib.py`: library of all commonly used movement, reading, and testing functions

`timer.py`: for counting elapsed time

