import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

# DR (Dubinin-Radushkevich) plot
result_dict = pygaps.dr_plot(isotherm, verbose=True)
#result_dict = pygaps.dr_plot(isotherm, limits=[0,0.1], verbose=True)

# plot
fig1 = plt.figure(1)
fig1.savefig('./plot/DR-plot.jpg')
#plt.show()

# import pprint
# pprint.pprint(result_dict)
