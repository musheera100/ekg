PROJECT UPDATE 1:
#To generate the plot outputs for our first software implementation, run the ECG.py file in this repo. 

The code we've been working with is almost entirely based on this implementation: https://github.com/tejasa97/ECG-Signal-Processing  

PROJECT UPDATE 2: See Project Update 2 Folder.

Filter_Testing.m is the MATLAB file used to derive the filter coefficients, and includes the iniital implementation of the DFII and DFI filter functions.

Filter_DFIIt.py contains the Python equivalent functions for the DFII and DFI filter functions in Filter_Testing.m

filter_df2t.cpp contains the C function for the DFII filter function

filter_df2t.h is a header file for filter_df2t.cpp

IIR_Filter_testb.cpp is a testbench for filter_df2t.cpp

ECG_good.csv is the input ECK sequence used in the test bench, and ECG_out_gold.csv is the Golden Output for the test bench

sma.m contains some additonal functions for further processing of the ECG signal after filtering
