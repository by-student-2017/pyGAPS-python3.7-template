import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
isotherm.print_info()

# t-plot
result_dict = pygaps.t_plot(isotherm, verbose=True)
#result_dict = pygaps.t_plot(isotherm, thickness_model='Harkins/Jura',
#              limits=(0.3,0.44), verbose=True)

# plot
plt.show()

import pprint
pprint.pprint(result_dict)

#import pandas as pd
#df = pd.DataFrame(result_dict)
#df.to_csv("result_t-plot.csv", index=False)