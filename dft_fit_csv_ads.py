import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
isotherm.print_info()

# fitting on DFT kernel
result_dict_dft = pygaps.psd_dft(
    isotherm,
    kernel='DFT-N2-77K-carbon-slit',
    #branch='des',
    #bspline_order=5,
    verbose=True)

# plot
plt.show()

#import pprint
#pprint.pprint(result_dict_dft)

import pandas as pd
df = pd.DataFrame(result_dict_dft)
#df.to_csv("result_dft_ads.csv", index=False)

# set init of ds
dfds = pd.DataFrame(df.assign(ds=0.0e0, tds=0.0e0))

import numpy as np

# convert pandas to numpy array
ndfds = dfds.to_numpy()

# calculate ds and Cumulative ds
ultramicropore = 0.0
supermicropore = 0.0
micropore = 0.0
macropore = 0.0
#
ndfds[0,3] = (ndfds[0,2] - 0.0)/(ndfds[0,0]/2.0)*1000.0
ndfds[0,4] = ndfds[0,3]
for num in range(1,len(ndfds)):
  ndfds[num,3] = (ndfds[num,2] - ndfds[num-1,2])/(ndfds[num,0]/2.0)*1000.0
  ndfds[num,4] = ndfds[num-1,4] + ndfds[num,3]
  if (ndfds[num,0] < 0.7):    # < 0.7 nm: ultra-micropore
    ultramicropore = ultramicropore + ndfds[num,3]
  elif (ndfds[num,0] < 2.0):  # 0.7 - 2 nm: super-micropore
    supermicropore = supermicropore + ndfds[num,3]
  elif (ndfds[num,0] < 50.0): # 2 - 50 nm: micropore
    micropore = micropore + ndfds[num,3]
  else:                       # > 50 nm: macropore
    macropore = macropore + ndfds[num,3]
#
print("ultra-micropore: %7.2f [m^2/g] (w < 0.7 nm)" % (ultramicropore))
print("super-micropore: %7.2f [m^2/g] (0.7 =< w < 2.0 nm)" % (supermicropore))
print("micropore: %7.2f [m^2/g], Attention!!! limited range (2-10 nm)" % (micropore))
print("total ds: %7.2f [m^2/g], Attention!!! limited range (0.4 =< w =< 10 nm)" % (ndfds[len(ndfds)-1,4]))
#
x = ndfds[:,0]
y = ndfds[:,3]
y2 = ndfds[:,4]
#
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()
ax1.plot(x, y, label="ds", color='black')
ax1.set_ylabel('Incremental Surface Area $(m^{2}/g)$')
ax2.plot(x, y2, label="Cumulative ds", color='red', linestyle="--")
ax2.set_ylabel('Cumulative ds $(m^{2}/g)$') 
#
plt.title("PSD plot NLDFT (carbon slit)")
plt.xlabel("Pore size (nm)")
plt.xscale("log")
plt.grid()
plt.show()

# set name of columns
ndf = pd.DataFrame(ndfds)
ndf.columns = ['pore_widths_nm', 'pore_distribution', 'pore_volume_cumulative_cm^3g^-1', 'ds_m^2g^-1', 'cumulative_ds']

# output window and excel file
import pprint
pprint.pprint(ndf)
ndf.to_csv("result_dft_ads.csv", index=False)