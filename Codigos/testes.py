
import matplotlib.pyplot as plt
import scipy.stats as stats

x = list(range(10))
y = list(range(10,20))


stat, p = stats.ks_2samp(x, y)

print(stat, p)