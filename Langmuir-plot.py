import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

pygaps.area_langmuir(isotherm, verbose=True)
#pygaps.area_langmuir(isotherm, limits=(0.05, 0.3), verbose=True)
fig1 = plt.figure(1)
fig1.savefig('./plot/Langmuir-plot.jpg')
plt.show()