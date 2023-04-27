import csv
import matplotlib.pyplot as plt

# Defining Direct Form II Filter Function
# - - - - - - - - - - - - - - - - - - - - - - - - - -
def filter_df2t(b, a, x):
    #Initializing Shift Register
    k = max(len(a), len(b))
    shift_reg_v = [0 for i in range(k)]

    #Initializeing output sequence
    y = [0 for i in range(len(x))]

    #Looping through data to be filtered
    for i in range(len(x)):
        y[i] = b[0]*x[i] + shift_reg_v[k-2]
        # Multiply-Accumulate Loop
        for j in range(k-2, 0, -1):
            shift_reg_v[j] = shift_reg_v[j-1] + x[i]*b[k-j-1] - y[i]*a[k-j-1]
        shift_reg_v[0] = x[i]*b[k-1] - y[i]*a[k-1]
    return y

# Testing Direct Form II Filter Function
# - - - - - - - - - - - - - - - - - - - - - - - - - -
# Reading in sample data from .csv
csv_file_path = "ECG_good.csv"
data = []
with open(csv_file_path, newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        data.append(row)

data = data[0]
ecg_sig = [float(x) for x in data[0:10000]]
x = [i for i in range(len(ecg_sig))]

# Defining Filter Coefficients
b = [0.000000495352235,0.000002972113413,0.000007430283531,0.000009907044708,
     0.000007430283531,0.000002972113413,0.000000495352235]
a = [1, -5.271918566723349, 11.619927717930022, -13.702695926669762,
     9.116066297447906, -3.243419845060293, 0.482072025618542]

# Filtering the signal
ecg_filt = filter_df2t(b, a, ecg_sig)

# Plotting the filtered and unfiltered waveforms
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(12, 3))

ax1.plot(x, ecg_sig)
ax1.set_title('Unfiltered ECG')
ax1.set_xlabel("Time")
ax1.set_ylabel("Amplitude (mV)")

ax2.plot(x, ecg_filt)
ax2.set_title('Filtered ECG (DFIIt)')
ax2.set_xlabel("Time")
ax2.set_ylabel("Amplitude (mV)")
plt.show()