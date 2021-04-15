import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

# CarbonBlack
def carbon_model(relative_p):
    return 0.88*(relative_p**2) + 6.45*relative_p + 2.98

# t-plot
result_dict = pygaps.t_plot(isotherm, thickness_model=carbon_model, limits=(3.5,5.5), verbose=True)
#result_dict = pygaps.t_plot(isotherm, thickness_model=carbon_model,
#              limits=(0.3,0.44), verbose=True)

# plot
fig1 = plt.figure(1)
fig1.savefig('./plot/t-plot_Ref_CB_a3.jpg')
plt.show()

import pprint
pprint.pprint(result_dict)

#import pandas as pd
#df = pd.DataFrame(result_dict)
#df.to_csv("result_t-plot.csv", index=False)