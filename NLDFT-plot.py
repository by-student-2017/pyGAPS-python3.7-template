import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

# fitting on DFT kernel
result_dict_dft = pygaps.psd_dft(
    isotherm,
    kernel='DFT-N2-77K-carbon-slit',
    #branch='des',
    #bspline_order=5,
    verbose=True)

# plot
fig1 = plt.figure(1)
fig1.savefig('./plot/NLDFT_No1.jpg')
fig2 = plt.figure(2)
fig2.savefig('./plot/NLDFT_No2.jpg')
plt.show()

# import pprint
# pprint.pprint(result_dict_dft)

import pandas as pd
df = pd.DataFrame(result_dict_dft)
df.to_csv("result_NLDFT.csv", index=False)