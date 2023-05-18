# PiezoProject_UMich
Repository for Python code relating to the University of Michigan piezo positioner test stand.

Last updated: 05/18/2023

# Files

If there are two files with the same name except one is a jupyter notebook, assume they serve the same purpose.

`AutoCircleCopyRS.py`: function to move the spine along the maximum range 

`AutoDriftTest.ipynb`: notebook for looking at drift and angular alignment of axis

`AutoFitCircle.py`: function to move the spine along maximum range and return a best fit of said range 

`AutoVelocityTest.py`: test the distance moved over time for standard movement calibs 

`AutoXYTest.py`: generate a table of random points and attempt each once, returns csv of goals and finals

`AutoXYTestWinCond.py`: generate a table of random points and attempt to get within an error radium given a maximum attempt limit, returns csv of goals paired with all finals 

`GrabLocation.py`: function to return the location of the tip of the spine 

`LiveVid.py`: show a live image of the spine tip 

`MicroMovements.py`: movements calibrated for the smallest distance the spine will move 

`Movements.py`: standard move type, used based on dist/time for standard wave 

`MovementsSteps.py`: same configuration as standard move, but the argument given is number of pulses

`PiezoGUI.py`: user interface for extensive testing

`PixMovements.py`: not used anymore, used to be the smallest move type before sub-pixel measurement

`PlotAutoDriftTest.ipynb`: used to plot a drift test 

`PlotXYTest.ipynb`: used to plot a basic XY test

`PlotXYTestWinCond.ipynb`: used to plot XY test with the win condition

`StillErrorOverRange.ipynb`: used to test the detection error at multiple point across the spine's range

`Testing.ipynb`: for testing the waveform and corresponding motion 

`TinyMoveTesting.ipynb`: for testing the smaller moves

`TinyMovements.py`: the medium sized move, calibrated based on regular move but changes frequency for more precision

`WaveformTesting-Copy1.ipynb`: more waveform testing code 

`WaveformTesting.ipynb`: older waveform testing code 

`Waveform_autotest.py`: function for easy repeated testing of movement from waveform

`config_constants.py`: contains all numerical values that describe the setup and calibrated moves 

`datacollectsoftware-CopyRS-OLD.ipynb`: the old way of detecting the spine, terrible but saved for posterity

`datacollectsoftware-CopyRS.ipynb`: new way to detect position with minimal error

`move_by_XY.py`: moves the spine by an XY amount, choses move type based on distance 

`move_by_XYold.py`: older movement code

`timer.py`: for counting elapsed time

