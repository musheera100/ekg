This folder contains all of the code for our final project.

1. The folder labelled JUPYTER_NOTEBOOK contains the final working Jupyter notebook, 
as well as all the files needed in order to implement the lowpass and highpass filter overlays. 
It also includes the ECG_good.csv file that was used as an input for the notebook. 

2. The folder labelled MATLAB_CODE contains the MATLAB code used to generate the filter a and b coefficients, 
and to determine the error of the FPGA filter implementation. 
The code reads in the csv output from the FPGA testbench, and compares it to the output of the software filter. 
The Direct Form II Transposed filter function in this file was the basis for our python and C filter implementations. 
Also included in this folder is a subfolder titled "Dialing_In_coefficient_Precision," 
which contains FPGA filter outputs that we generated while testing variations on the ap_fixed data type 
for our filter coefficients and tapped delay line.

3. The folder labelled PYTHON_CODE contains the Python implementation of the 
Direct Form II Transposed filter function which was used to benchmark 
hardware performance in the Jupyter notebook and source code for arrythmia detection.

4. The folder labelled VITIS_C_CODE contains three subfolders: 
one for the lowpass filter (.cpp and .h), 
one for the highpass filter (.cpp and .h), 
and one with an older version of the lowpass filter and the testbench used to 
verify the output and export the results to a csv so it could be read into MATLAB.

5. The folder labelled VIVADO_FILES contains various files related to the 
VIVADO implementations of the lowpass and highpass filters. 
This includes block diagram pdfs, .coe files, and overlay files (.tcl, .bit, and .hwh).

6. Our Final Project Presentation
