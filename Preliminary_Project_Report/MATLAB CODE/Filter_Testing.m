%//////////////////////////////////////////////////////////////////////////
% 3/26/2023
% Program for creating and verifying custom buttersworth filters for ECG
% signal processing. Includes functions to filter signals with Normal and
% Transposed DF2 structures. 
%//////////////////////////////////////////////////////////////////////////

%Reading in Data from Bitalino Measurement .txt files:
Ntotal = 30000;
fraction = 0.5; % fraction of samples to keep (runs slower with more samples)
N = Ntotal*fraction; % # samples to keep
fs = 1000; %Sampling freq

% Reading in data from the .txt files:
%ECG_raw = (importdata('day1-1.txt')).data(1:N,6); %/(2.^10))-0.5)*3.3/1100;

% Intitial data scaling (samples to V). 
% Scaling by 10 to make it a more typical ECG range
% ECG_raw = 10000*((ECG_raw./(2.^10))-0.5)*(3.3/1100);
% ECG_raw = ECG_raw.';

%Adding Noise to the signal
% n = 0:N-1;
% w_EMG = 257*2*pi;
% w_mains = 60*2*pi;
% w_baseline_wander1 = 0.05*2*pi;
% w_baseline_wander2 = 0.07*2*pi;
% 
% Noise = 0.7*sin(w_EMG*n/fs) + sin(w_mains*n/fs) + 4*sin(w_baseline_wander1*n/fs) + 4*cos(w_baseline_wander2*n/fs);
% ECG = ECG_raw + Noise;

%ECG_scaled = int32(ECG*1000*1000);
ECG_scaled = importdata('ECG_good.csv');
ECG_scaled = double(int32(ECG_scaled*1000));
FPGA_OUTPUT = importdata('ECG_out.csv');
%ECG_INPUT = ECG_scaled(1:10)

%csvwrite('ECG_good.csv',ECG,1,0)

% Deriving LP Buttersworth Filter coefficients
fc1 = 30;
[b1,a1] = butter(6,fc1/(fs/2),'low')
b1_int = int32(b1*(2^24));
a1_int = int32(a1*(2^24));


% Deriving HP Buttersworth Filter coeffcients
fc2 = 0.5;
[b2,a2] = butter(1,fc2/(fs/2),'High')
b2_int = int32(b2*(2^24));
a2_int = int32(a2*(2^24));

% Filtering the ECG Signal
ECG_LP_Auto = filter(b1,a1,ECG_scaled);
ECG_BP_Auto = filter(b2,a2,ECG_LP_Auto);

ECG_LP = filter_FPGA_DF2t(b1,a1, ECG_scaled)/1000;
ECG_BP = filter_FPGA_DF2t(b2,a2,ECG_LP);

%LP_OUTPUT = ECG_LP(1:10);
INPUT_1_ECG_SCALED = ECG_scaled(1)
format long
disp("b1[0] ")
disp(b1(1));

disp("b1[0]*1st input")
disp(int32(ECG_scaled(1)*b1(1)))

disp("First value of ECG Input")
disp(ECG_scaled(1))

disp("ECG LP Output 1st Term: ")
disp(ECG_LP(1))


%Plotting "Golden" data
csvwrite('ECG_out_gold.csv', ECG_LP)

%Plotting Filter Outputs
%//////////////////////////////////////////////////////////////////////////
f1 = figure("Position",[0,0,100,50]*72); % use a taller and wider figure size
n = 0:(1/fs):(N-(1/fs))/fs; %0 to 30 seconds, in increments of 1ms for Fs = 1kHz

p1 = subplot(5,1,1);
plot(n,ECG_scaled);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('Raw ECG Signal');
xlim([0 (N/fs)*fraction]);
ylim([-10000 10000]);

p7 = subplot(5,1,2);
plot(n,ECG_LP);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('MATLAB LP FILTER OUTPUT (GOLDEN OUTPUT)');
xlim([0 (N/fs)*fraction]);
ylim([-8 8]);

p6 = subplot(5,1,3);
plot(n,FPGA_OUTPUT);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('FPGA LP FILTER OUTPUT');
xlim([0 (N/fs)*fraction]);
ylim([-8 8]);

p5 = subplot(5,1,4);
plot(n,ECG_LP-FPGA_OUTPUT);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('FPGA FILTER ERROR');
xlim([0 (N/fs)*fraction]);
ylim([-0.1 0.1]);

p8 = subplot(5,1,5);
plot(n,ECG_BP);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG BP Filter w/ HP DF2t function');
xlim([0 (N/fs)*fraction]);
ylim([-8 8]);


%//////////////////////////////////////////////////////////////////////////
% Normal DF2 Filter Function
function y = filter_FPGA_DF2n_SCALED(b,a,x)
sf = 2^25; %2^25; %defining scaling factor

b = double(int32(b*sf)); % scaling up coefficients
a = double(int32(a*sf));
%b = int32(b*sf) % scaling up coefficients
%a = int32(a*sf)

% finding K = # delay terms needed for DFII s``tructure
N = length(a); 

M = length(b); 
K = max(N,M);
shift_reg_in = zeros(K,1); % Defines a shift register of length K
shift_reg_out = zeros(K,1);
y = zeros(length(x),1); % Defining output y array

% Looping through x data to be filtered
for i = 1:length(x)
    x_i = x(i); % Current value of x
    % Tapped Delay Line
    for j = K:-1:2
        %display(["j: " j])
        shift_reg_in(j) = shift_reg_in(j-1);
        shift_reg_out(j) = shift_reg_out(j-1);
    end
    shift_reg_in(1) = x_i;

    % Multiply-Accumulate Loop
    y_i = shift_reg_in(1)*b(1); %Pulling out b0 term, since a0 always 1
    for k = K:-1:2
        y_i = y_i - a(k)*shift_reg_out(k) + b(k)*shift_reg_in(k);
    end
    y_i = y_i/sf; %scaling down output
    shift_reg_out(1) = y_i;
    y(i) = y_i;
end
y = y.';
disp('filtering with DF2 normal structure done')
end

%//////////////////////////////////////////////////////////////////////////
% Transposed DF2 Filter Function
function y = filter_FPGA_DF2t_SCALED(b,a,x)
% finding K = # delay terms needed for DFII structure
sf = 2^25;
b = double(int64(b*sf));
a = double(int64(a*sf));
N = length(a); 
M = length(b); 
K = max(N,M);
shift_reg_v = zeros(K-1,1); % Defines a shift register of length K-1
y = zeros(length(x),1); % Defining output y array

% Looping through x data to be filtered
for i = 1:length(x)
    x_i = x(i); % Current value of x

    y_i = int64((b(1)*x_i + shift_reg_v(K-1))/(sf));
    % Tapped Delay Line + MAC
    for j = K-1:-1:2
        %display(["j: " j])
        shift_reg_v(j) = shift_reg_v(j-1)+x_i*b(K-j+1)-y_i*a(K-j+1);
    end
    shift_reg_v(1) =  x_i*b(K) - y_i*a(K);
    y(i) = y_i;
end
y = y.';
disp('filtering with DF2 transposed structure done')
end

%//////////////////////////////////////////////////////////////////////////


%//////////////////////////////////////////////////////////////////////////
% Transposed DF2 Filter Function
function y = filter_FPGA_DF2t(b,a,x)
% finding K = # delay terms needed for DFII structure
N = length(a); 
M = length(b); 
K = max(N,M);
shift_reg_v = zeros(K-1,1); % Defines a shift register of length K-1
y = zeros(length(x),1); % Defining output y array

% Looping through x data to be filtered
for i = 1:length(x)
    x_i = x(i); % Current value of x

    y_i = b(1)*x_i + shift_reg_v(K-1);
    % Tapped Delay Line + MAC
    for j = K-1:-1:2
        %display(["j: " j])
        shift_reg_v(j) = shift_reg_v(j-1)+x_i*b(K-j+1)-y_i*a(K-j+1);
    end
    shift_reg_v(1) =  x_i*b(K) - y_i*a(K);
    y(i) = y_i;
end
y = y.';
disp('filtering with DF2 transposed structure done')
end

%//////////////////////////////////////////////////////////////////////////



