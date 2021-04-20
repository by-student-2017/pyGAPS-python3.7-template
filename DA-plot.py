import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

# DA (Dubinin-Astakov) plot
#result_dict = pygaps.da_plot(isotherm, limits=[0,0.1], exp=2.3, verbose=True)
result_dict = pygaps.da_plot(isotherm, limits=[0, 0.1], exp=None, verbose=True)

# plot
fig1 = plt.figure(1)
fig1.savefig('./plot/DA-plot.jpg')
#plt.show()

# import pprint
# pprint.pprint(result_dict)
