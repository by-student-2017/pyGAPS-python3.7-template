import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
isotherm.print_info()

# Langmuir plot
result_dict = pygaps.area_langmuir(isotherm, verbose=True)
#result_dict = pygaps.area_langmuir(isotherm, limits=(0.05, 0.3), verbose=True)

# plot
plt.show()

# import pprint
# pprint.pprint(result_dict)

import pandas as pd
df = pd.DataFrame(result_dict)
df.to_csv("result_Langmuir.csv", index=False)