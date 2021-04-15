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
fig1 = plt.figure(1)
fig1.savefig('./plot/NLDFT_Fit.jpg')
fig2 = plt.figure(2)
fig2.savefig('./plot/NLDFT.jpg')
plt.show()

#import pprint
#pprint.pprint(result_dict_dft)

import pandas as pd
df = pd.DataFrame(result_dict_dft)
#df.to_csv("result_dft_ads.csv", index=False)

# set init of ds
dfds = pd.DataFrame(df.assign(ds=0.0e0))

import numpy as np

# convert pandas to numpy array
ndfds = dfds.to_numpy()

# calculate ds
ndfds[0,3] = (ndfds[0,2] - 0.0)/ndfds[0,0]*1000.0
for num in range(1,len(ndfds)):
  ndfds[num,3] = (ndfds[num,2] - ndfds[num-1,2])/ndfds[num,0]*1000.0

# set name of columns
ndf = pd.DataFrame(ndfds)
ndf.columns = ['pore_widths_nm', 'pore_distribution', 'pore_volume_cumulative_cm^3g^-1', 'ds_m^2g^-1']

# output window and excel file
import pprint
pprint.pprint(ndf)
ndf.to_csv("result_dft_ads.csv", index=False)