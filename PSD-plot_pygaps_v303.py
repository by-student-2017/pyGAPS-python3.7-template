import pygaps
import matplotlib.pyplot as plt

# HK, HK_MOF
micro_method = "HK"

# DH, pygaps-DH, BJH
meso_method  = "BJH"

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

# PSO (Pore size distribution)
# https://pygaps.readthedocs.io/en/master/examples/psd.html

# NLDFT
result_dict_dft = pygaps.psd_dft(
    isotherm,
    kernel='DFT-N2-77K-carbon-slit',
    verbose=False)


if micro_method == "HK":
    # HK (Horvath-Kawazoe) method
    result_dict_micro = pygaps.psd_microporous(
        isotherm,
        psd_model='HK',
        verbose=False)

elif micro_method == "HK-CY":
    # Cheng-Yang modification of HK (Horvath-Kawazoe) method
    result_dict_micro = pygaps.psd_microporous(
        isotherm,
        psd_model='HK-CY',
        verbose=False)

elif micro_method == "HK_MOF":
    # HK method for MOF
    adsorbate_params = {
        'molecular_diameter': 0.3,
        'polarizability': 1.76e-3,
        'magnetic_susceptibility': 3.6e-8,
        'surface_density': 6.71e+18,
        'liquid_density': 0.806,
        'adsorbate_molar_mass': 28.0134
    }
    #
    result_dict_micro = pygaps.psd_microporous(
        isotherm,
        psd_model='HK',
        adsorbent_model='AlSiOxideIon',
        adsorbate_model=adsorbate_params,
        verbose=False)

elif micro_method == "RY":
    # RY (Rege-Yang) adapted model
    result_dict_micro = pygaps.psd_microporous(
        isotherm,
        psd_model='RY',
        verbose=False)

elif micro_method == "RY-CY":
    # Cheng-Yang modification of RY (Rege-Yang) adapted model
    result_dict_micro = pygaps.psd_microporous(
        isotherm,
        psd_model='RY-CY',
        verbose=False)

else:
    print('ERROR!:')


if meso_method == "BJH":
    # BJH (Barrett, Joyner and Halenda) method
    result_dict_meso = pygaps.psd_mesoporous(
        isotherm,
        psd_model='BJH',
        pore_geometry='cylinder',
        verbose=False)

elif meso_method == "pygaps-DH":
    # pygaps-DH
    result_dict_meso = pygaps.psd_mesoporous(
        isotherm,
        psd_model='pygaps-DH',
        pore_geometry='slit',
        verbose=False)

elif meso_method == "DH":
    # DH (KJS = Kruck-Jaroniec-Sayari correction of the Kelvin model)
    result_dict_meso = pygaps.psd_mesoporous(
        isotherm,
        psd_model='DH',
        pore_geometry='cylinder',
        branch='ads',
        thickness_model='Halsey',
        kelvin_model='Kelvin-KJS',
        verbose=False)
else:
    print('ERROR!:')


# Comparing all the PSD methods
#from pygaps.graphing.calcgraph import psd_plot # version 2.0.2
from pygaps.graphing.calc_graphs import psd_plot # version 3.0.3
ax = psd_plot(result_dict_dft['pore_widths'], result_dict_dft['pore_distribution'],
              method='comparison', labeldiff='NLDFT', labelcum=None, left=0.4, right=8)
ax.plot(result_dict_micro['pore_widths'], result_dict_micro['pore_distribution'], label='microporous ('+micro_method+')')
ax.plot(result_dict_meso['pore_widths'], result_dict_meso['pore_distribution'], label='mesoporous ('+meso_method+')')
ax.legend(loc='best')

# plot
fig1 = plt.figure(1)
fig1.savefig('./plot/PSD-plot.jpg')
#plt.show()

# import pprint
# pprint.pprint(result_dict)

#import pandas as pd
#df = pd.DataFrame(result_dict)
#df.to_csv("result_PSO.csv", index=False)