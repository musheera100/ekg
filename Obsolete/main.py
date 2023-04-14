# //////////////////////////////////////////////////////////////////////////
# 3/27/2023
# Defines Filter_DFIIt function
# Filters a signal using a transposed DFII structure
# //////////////////////////////////////////////////////////////////////////
import Filter_DFIIt
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
pi = math.pi

# Reading in Data
ntotal = 30000
fraction = 0.5  # fraction of samples to keep (runs slower with more samples)
samples = int(ntotal*fraction)  # number of samples to keep
fs = 1000  # Sampling frequency

# Reading in data from the .txt file:
# importdata('day1-1.txt').data(1:samples,6); %/(2.^10))-0.5)*3.3/1100;

#filename = 'day1-1.txt'

file = open("ECG_good.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

ECG_raw = [0]*len(data[0])

for i in range(len(data[0])):
    ECG_raw[i] = data[0][i]

# Initial data scaling (samples to V).
# Scaling by 10 to make it a more typical ECG range

for i in range(len(ECG_raw)):
    ECG_raw[i] = float(ECG_raw[i])
    #ECG_raw[i] = 1000000*((float(ECG_raw[i])/(pow(2, 10)))-0.5)*(3.3/1100)
#print(ECG_raw[0])

# Adding Noise to the signal
#n = [0]*(samples-1)
w_EMG = 257*2*pi
w_mains = 60*2*pi
w_baseline_wander1 = 0.05*2*pi
w_baseline_wander2 = 0.07*2*pi

ECG = [0]*len(ECG_raw)
for i in range(len(ECG_raw)):
    Noise = 0.7*math.sin(w_EMG*i/fs) + math.sin(w_mains*i/fs)
    Noise = Noise + 4*math.sin(w_baseline_wander1*i/fs) + 4*math.cos(w_baseline_wander2*i/fs)
    ECG[i] = ECG_raw[i] + 0.0004*Noise



# Deriving LP Butterworth Filter coefficients
# Coefficients for fc = 30Hz, n = 6 LP Filter
b1 = [0.0495*1.0e-05, 0.2972*1.0e-05, 0.7430*1.0e-05, 0.9907*1.0e-05, 0.7430*1.0e-05, 0.2972*1.0e-05, 0.0495*1.0e-05]
print(b1)
a1 = [1.0000, -5.2719, 11.6199, -13.7027, 9.1161, -3.2434, 0.4821]
print(a1)

# Deriving HP Butterworth Filter coefficients
# Coefficients for fc = 0.5Hz, n = 1 HP Filter
b2 = [0.9984, -0.9984]
a2 = [1.0000, -0.9969]

# Filtering the ECG Signal
test = [3.7949, 4.9222, 4.5084, 4.0975, 4.9791, 5.4940, 4.4490, 3.6770, 4.2008, 4.2620]
print(test)
ECG_LP = Filter_DFIIt.filter_fpga_df2t(b1, a1, ECG_raw)
print(ECG_LP)
#ECG_BP = Filter_DFIIt.filter_fpga_df2t(b2, a2, ECG_LP)

# Plotting "Golden" data
# //////////////////////////////////////////////////////////////////////////
fig1 = plt.figure()
ax1 = fig1.add_subplot(311)
ax1.plot(ECG_raw, color='r', linewidth=0.7)
ax1.set_title('Before filtering')
plt.xlim([0, 7.5*1000])

ax2 = fig1.add_subplot(312)
ax2.plot(ECG_LP, color='r', linewidth=0.7)
ax2.set_title('After filtering with LP')
plt.xlim([0, 7.5*1000])

ax3 = fig1.add_subplot(313)
ax3.plot(ECG_raw, color='r', linewidth=0.7)
ax3.set_title('After filtering with HP')
plt.xlim([0, 7.5*1000])

plt.show()


"""
f1 = figure("Position",[0,0,100,50]*72) # use a taller and wider figure size
n = 0:(1/fs):(N-(1/fs))/fs #0 to 30 seconds, in increments of 1ms for Fs = 1kHz


p1 = subplot(4,2,1);
plot(n,ECG_raw);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG Unedited');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

p2 = subplot(4,2,3);
plot(n,ECG);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG With Noise');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

p3 = subplot(4,2,5);
plot(n,ECG_LP_Auto);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG LP Filter');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

p4 = subplot(4,2,7);
plot(n,ECG_BP_Auto);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG BP Filter');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

# Plotting data filtered with custom functions
# /////////////////////////////////////////////////////////////////////////

p5 = subplot(4,2,2);
plot(n,ECG_raw);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG Unedited');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

p6 = subplot(4,2,4);
plot(n,ECG);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG With Noise');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

p7 = subplot(4,2,6);
plot(n,ECG_LP);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG LP Filter w/ LP DF2n Function');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

p8 = subplot(4,2,8);
plot(n,ECG_BP);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG BP Filter w/ HP DF2t function');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);

"""


