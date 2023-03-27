# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import wfdb
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show

# Functions defined up here
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

if __name__ == '__main__': # Main function
    print_hi('PyCharm')
    ecg_record = wfdb.rdheader('100', pn_dir='mitdb')
    # record = wfdb.rdrecord('lobachevsky-university-electrocardiography-database-1.0.1/data/1', sampfrom=800, channels=[0])
    signals, fields = wfdb.rdsamp('lobachevsky-university-electrocardiography-database-1.0.1/data/1', sampfrom=800, channels=[0])
    figure(4)
    plot(signals)
    # ------------------------------------------------
    # Create a signal for demonstration.
    # ------------------------------------------------

    sample_rate = 500.0
    nsamples = 2000
    t = arange(nsamples) / sample_rate
    x = cos(2*pi*1*t) + 5*sin(2*pi*60*t)

    # Modifed from: https://scipy-cookbook.readthedocs.io/items/FIRFilter.html
    # ------------------------------------------------
    # Create a FIR filter and apply it to x.
    # ------------------------------------------------

    # The Nyquist rate of the signal.
    nyq_rate = sample_rate / 2.0

    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate.  We'll design the filter
    # with a 5 Hz transition width.
    width = 5.0 / nyq_rate

    # The desired attenuation in the stop band, in dB.
    ripple_db = 60.0

    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)
    print(f'N, {N}')
    # The cutoff frequency of the filter.
    cutoff_low_hz = 0.2
    cutoff_high_hz = 40
    # (cutoff_low_hz/nyq_rate, cutoff_high_hz/nyq_rate)
    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, (cutoff_low_hz/nyq_rate, cutoff_high_hz/nyq_rate), window=('kaiser', beta), pass_zero='bandpass')

    # Use lfilter to filter x with the FIR filter.
    filtered_x = lfilter(taps, 1.0, x)


    # ------------------------------------------------
    # Plot the FIR filter coefficients.
    # ------------------------------------------------

    figure(1)
    plot(taps, 'bo-', linewidth=2)
    title('Filter Coefficients (%d taps)' % N)
    grid(True)

    # ------------------------------------------------
    # Plot the magnitude response of the filter.
    # ------------------------------------------------

    figure(2)
    clf()
    w, h = freqz(taps, worN=8000)
    plot((w / pi) * nyq_rate, absolute(h), linewidth=2)
    xlabel('Frequency (Hz)')
    ylabel('Gain')
    title('Frequency Response')
    ylim(-0.05, 1.05)
    grid(True)

    # Upper inset plot.
    # ax1 = axes([0.42, 0.6, .45, .25])
    # plot((w / pi) * nyq_rate, absolute(h), linewidth=2)
    # xlim(0.2, 50)
    # ylim(0.8, 1.100)
    # grid(True)

    # Lower inset plot
    #ax2 = axes([0.42, 0.25, .45, .25])
    # plot((w / pi) * nyq_rate, absolute(h), linewidth=2)
    # xlim(12.0, 20.0)
    # ylim(0.0, 0.0025)
    #grid(True)

    # ------------------------------------------------
    # Plot the original and filtered signals.
    # ------------------------------------------------

    # The phase delay of the filtered signal.
    delay = 0.5 * (N - 1) / sample_rate

    figure(3)
    # Plot the original signal.
    plot(t, x)
    # Plot the filtered signal, shifted to compensate for the phase delay.
    plot(t - delay, filtered_x, 'r-')
    # Plot just the "good" part of the filtered signal.  The first N-1
    # samples are "corrupted" by the initial conditions.
    plot(t[N - 1:] - delay, filtered_x[N - 1:], 'g', linewidth=4)
    title('Orginal waveform (blue) vs. Filtered waveform (green)')
    xlabel('t')
    grid(True)

    show()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
