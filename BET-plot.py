import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
isotherm.print_info()

# BET plot
result_dict = pygaps.area_BET(isotherm, verbose=True)

# plot
plt.show()

# import pprint
# pprint.pprint(result_dict)

import pandas as pd
df = pd.DataFrame(result_dict)
df.to_csv("result_BET.csv", index=False)