import pygaps
import matplotlib.pyplot as plt

# create the path (sample)
path = r'case.csv'

# create the path (reference)
path_ref = r'CarbonBlack_ref.csv'

# import the isotherm (sample)
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

# import the isotherm (reference)
isotherm_ref = pygaps.isotherm_from_csv(path_ref)
#isotherm_ref.print_info()

# create model for "ERROR!: A value in x_new is below the interpolation range."
model = pygaps.ModelIsotherm.from_pointisotherm(isotherm_ref, model='BET')
pygaps.plot_iso([isotherm_ref, model], branch='ads')
##plt.show()
#model.print_info(logx=False)
import numpy
pressure_range=numpy.linspace(1.0e-09, 1.00, 1000)
new_point_isotherm=pygaps.PointIsotherm.from_modelisotherm(
    model,
    pressure_range,
    )
path_model = r'model.csv'
pygaps.isotherm_to_csv(new_point_isotherm, path_model)
path_model_ref = r'model.csv'
model_ref = pygaps.isotherm_from_csv(path_model_ref)

# alpha-s-plot
# https://pygaps.readthedocs.io/en/master/examples/alphas.html
result_dict = pygaps.alpha_s(isotherm, reference_isotherm=model_ref, limits=(2, 10), verbose=True)
#result_dict = pygaps.alpha_s(isotherm, reference_isotherm=model_ref, reference_area='BET', 
#                             reducing_pressure=0.4, limits=(0.6, 0.8), verbose=True)

# plot
fig1 = plt.figure(1)
fig1.savefig('./plot/alpha-s-plot_No1.jpg')
fig2 = plt.figure(2)
fig2.savefig('./plot/alpha-s-plot_No2.jpg')
#plt.show()

# import pprint
# pprint.pprint(result_dict)

#import pandas as pd
#df = pd.DataFrame(result_dict)
#df.to_csv("result_alpha-s-plot.csv", index=False)