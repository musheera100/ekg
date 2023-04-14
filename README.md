PRELIMINARY FINAL REPORT: See Preliminary Project Report Folder

- Folder is divided into MATLAB, VITIS/C code, and Python code

- MATLAB CODE contains the MATLAB program used to generate the a/b filter coefficients and generate the golden output, as well as all associated csv files.

- VITIS C CODE contains the Direct Form II Filter function .cpp file, as well as an associated header and testbench. It also contains all .csv files needed to run the testbench. The full VITIS project was also included as a .zip

- PYTHON CODE contains the python implementation of the Direct Form II Filter, for use in benchmarking the hardware implementation.It also includes a .csv for ECG data needed to run the program



PROJECT UPDATE 2: See Project Update 2 Folder.

Filter_Testing.m is the MATLAB file used to derive the filter coefficients, and includes the iniital implementation of the DFII and DFI filter functions.

Filter_DFIIt.py contains the Python equivalent functions for the DFII and DFI filter functions in Filter_Testing.m

filter_df2t.cpp contains the C function for the DFII filter function

filter_df2t.h is a header file for filter_df2t.cpp

IIR_Filter_testb.cpp is a testbench for filter_df2t.cpp

ECG_good.csv is the input ECG sequence used in the test bench, and ECG_out_gold.csv is the Golden Output for the test bench

sma.m contains some additonal functions for further processing of the ECG signal after filtering


PROJECT UPDATE 1:
#To generate the plot outputs for our first software implementation, run the ECG.py file in this repo. 

The code we've been working with is almost entirely based on this implementation: https://github.com/tejasa97/ECG-Signal-Processing  
