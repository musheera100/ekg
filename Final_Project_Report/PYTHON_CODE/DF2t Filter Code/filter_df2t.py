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
def sma(x,y,k):
    y = [0] * (k-1)
    for i in range(k-1, len(x)):
        window = x[i-k+1:i+1]
        y.append(sum(window) / k)


def arryth(x,p,tc,th,c,h):
    c = 0
    h = 0
    for i in range(len(x)):
        if(p[i]):
            if (x[i] > th):
                h+=1
            if(x[i]<tc):
                c+=1

#brute force finding location of peaks
def peaks(x,p):
    p = [-1]*len(x)
    for i in range(len(x)):
        if (x[i]>10 and x[i]>x[i-1] and x[i]>x[i+1]):
            p[i] = 1

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

b_hp = [0.998431665916719,-0.998431665916719]
a_hp = [1.000000000000000,-0.996863331833438]

# Filtering the signal
ecg_lp = filter_df2t(b_lp, a_lp, ecg_sig)
ecg_filt = filter_df2t(b_hp,a_hp,ecg_lp)

ECG_sq = [i**2 for i in ecg_filt]
k = 30
ECG_sma = [0]*len(ECG_sq)
sma(ecg_filt,ECG_sma,k)
p = [-1]*len(ECG_sq)
peaks(ECG_sq,p)
tc = 1.5
th = 1.5
c=0
h=0
arryth(ECG_sq,p,tc,th,c,h)
if(c>30):
    print("conduction disturbance detected")
if(h>0): 
    print("ST/T Change Detected")

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
