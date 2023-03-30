# //////////////////////////////////////////////////////////////////////////
# 3/27/2023
# Defines Filter_DFIIn and Filter_DFIIt functions
# Filters a signal using a transposed DFII structure
# //////////////////////////////////////////////////////////////////////////


# Transposed DFII Filter Function
# --------------------------------------------------------------------------
def filter_fpga_df2t(b, a, x):
    # finding K = # delay terms needed for DFII structure
    n = len(a)
    m = len(b)
    k = max(n, m)
    shift_reg_v = [0]*(k-1)  # Defines a shift register of length K-1
    y = [0]*len(x)  # Defining output y array

    # Looping through x data to be filtered
    for i in range(len(x)):
        x_i = x[i]  # Current value of x
        y_i = b[0]*x_i +

        # Tapped Delay Line + MAC
        for j in range(k-2, 0, -1):
            shift_reg_v[j] = shift_reg_v[j-1]+x_i*b[k-j-1]-y_i*a[k-j-1]
        shift_reg_v[0] = x_i*b[k-1] - y_i*a[k-1]
        y[i] = y_i
    return y


# Normal DF2 Filter Function
# --------------------------------------------------------------------------
def filter_fpga_df2n(b, a, x):
    # finding K = # delay terms needed for DFII structure
    n = len(a)
    m = len(b)
    k = max(n, m)
    shift_reg_in = [0]*(k-1)  # Defines a shift register of length K
    shift_reg_out = [0]*(k-1)
    y = [0]*len(x)  # Defining output y array

    # Looping through x data to be filtered
    for i in range(len(x)):
        x_i = x(i)  # Current value of x
        # Tapped Delay Line
        for j in range(k-1, -1, 2):
            shift_reg_in[j] = shift_reg_in[j-1]
            shift_reg_out[j] = shift_reg_out[j-1]
        shift_reg_in[1] = x_i

        # Multiply-Accumulate Loop
        y_i = shift_reg_in[1]*b[1]  # Pulling out b0 term, since a0 always 1
        for h in range(k-1, -1, 2):
            y_i = y_i - a[h]*shift_reg_out[h] + b[h]*shift_reg_in[h]
        shift_reg_out[1] = y_i
        y[i] = y_i
    return y
