def sma(x,y,k):
    y = [0] * (k-1)
    for i in range(k-1, len(x)):
        window = x[i-k+1:i+1]
        y.append(sum(window) / k)
