import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
isotherm.print_info()

# DH plot
result_dict = pygaps.psd_mesoporous(
    isotherm,
    psd_model='DH',
    branch='ads',
    pore_geometry='cylinder',
    thickness_model='Halsey',
    verbose=True,
)

# plot
plt.show()

# import pprint
# pprint.pprint(result_dict)

import pandas as pd
df = pd.DataFrame(result_dict)
df.to_csv("result_DH.csv", index=False)