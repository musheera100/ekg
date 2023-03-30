%Reading in Data from Bitalino Measurement .txt files:
Ntotal = 30000;
fraction = 0.5; % fraction of samples to keep (runs slower with more samples)
N = Ntotal*fraction; % # samples to keep
fs = 1000; %Sampling freq

% Reading in data from the .txt files:
ECG_raw = importdata('day1-1.txt').data(1:N,6); %/(2.^10))-0.5)*3.3/1100;

% Intitial data scaling (samples to V). 
% Scaling by 10 to make it a more typical ECG range
ECG_raw = 10000*((ECG_raw./(2.^10))-0.5)*(3.3/1100);
ECG_raw = ECG_raw.';

ECG_SMA = smax(ECG_raw, 30);



%Plotting "Golden" data
%//////////////////////////////////////////////////////////////////////////
f1 = figure("Position",[0,0,100,50]*72); % use a taller and wider figure size
n = 0:(1/fs):(N-(1/fs))/fs; %0 to 30 seconds, in increments of 1ms for Fs = 1kHz

p1 = subplot(4,2,1);
plot(n,ECG_raw);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG Unedited');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);


p2 = subplot(4,2,3);
plot(n,ECG_SMA);
xlabel('Time (seconds)');
ylabel('ECG Reading (mV)');
title('ECG With Moving Average');
xlim([0 (N/fs)*fraction]);
ylim([-6 6]);


function y = smax(x,k)
shift_reg = zeros(k,1); % Defines a shift register of length K-1
y = zeros(length(x),1); % Defining output y array

for i = 1:length(x)
    x_i = x(i);
    for j = k:2
        shift_reg(j) = shift_reg(j-1);
    end
    shift_reg(1) = x_i;
    y(i) = sum(shift_reg)/k;
end

end