import pygaps
import matplotlib.pyplot as plt

# create the path
path = r'case.csv'

# import the isotherm
isotherm = pygaps.isotherm_from_csv(path)
#isotherm.print_info()

# fitting on DFT kernel
result_dict_dft = pygaps.psd_dft(
    isotherm,
    kernel='DFT-N2-77K-carbon-slit',
    branch='des',
    #bspline_order=5,
    verbose=True)

# plot
fig1 = plt.figure(1)
fig1.savefig('./plot/NLDFT_DES_Fit.jpg')
fig2 = plt.figure(2)
fig2.savefig('./plot/NLDFT_DES.jpg')
plt.show()

# import pprint
# pprint.pprint(result_dict_dft)

import pandas as pd
df = pd.DataFrame(result_dict_dft)
#df.to_csv("result_dft_des.csv", index=False)

# set init of ds
dfds = pd.DataFrame(df.assign(ds=0.0e0, tds=0.0e0))

import numpy as np

# convert pandas to numpy array
ndfds = dfds.to_numpy()

# calculate ds and Cumulative ds
ultramicropore_s = 0.0
supermicropore_s = 0.0
micropore_s = 0.0
macropore_s = 0.0
#
ultramicropore_v = 0.0
supermicropore_v = 0.0
micropore_v = 0.0
macropore_v = 0.0
#
ndfds[0,3] = (ndfds[0,2] - 0.0)/(ndfds[0,0]/2.0)*1000.0
ndfds[0,4] = ndfds[0,3]
for num in range(1,len(ndfds)):
  ndfds[num,3] = (ndfds[num,2] - ndfds[num-1,2])/(ndfds[num,0]/2.0)*1000.0
  ndfds[num,4] = ndfds[num-1,4] + ndfds[num,3]
  if (ndfds[num,0] < 0.7):    # < 0.7 nm: ultra-micropore
    ultramicropore_s = ultramicropore_s + ndfds[num,3]
    ultramicropore_v = ndfds[num,2]
  elif (ndfds[num,0] < 2.0):  # 0.7 - 2 nm: super-micropore
    supermicropore_s = supermicropore_s + ndfds[num,3]
    supermicropore_v = ndfds[num,2] - ultramicropore_v
  elif (ndfds[num,0] < 50.0): # 2 - 50 nm: micropore
    micropore_s = micropore_s + ndfds[num,3]
    micropore_v = ndfds[num,2] - supermicropore_v - ultramicropore_v
  else:                       # > 50 nm: macropore
    macropore_s = macropore_s + ndfds[num,3]
    macropore_v = macropore_v + ndfds[num,2] - micropore_v - supermicropore_v - ultramicropore_v
#
print("***************************************************************************************************")
print("specific surface area and volume")
print("ultra-micropore: %7.2f [m2/g], %7.2f [cm3/g] (w < 0.7 nm)" % (ultramicropore_s, ultramicropore_v))
print("super-micropore: %7.2f [m2/g], %7.2f [cm3/g] (0.7 =< w < 2.0 nm)" % (supermicropore_s, supermicropore_v))
print("micropore:       %7.2f [m2/g], %7.2f [cm3/g] Attention!!! limited range (2-10 nm)" % (micropore_s, micropore_v))
print("total ds, V:     %7.2f [m2/g], %7.2f [cm3/g] Attention!!! limited range (0.4 =< w =< 10 nm)" % (ndfds[len(ndfds)-1,4], ndfds[len(ndfds)-1,2]))
print("***************************************************************************************************")
print("Note")
print("The BET method underestimates the specific surface area of ultra-micropore region.")
print("The BET method overestimates the specific surface area of super-micropore region by up to 50%.")
print("Since the BET model assumes multi-layer adsorption, it holds only for pores larger than mesopores. In addition, the pore surface area tends to be overestimated because the interaction from the solid surface acting on the second and subsequent layers is ignored. ")
print("total ds: %7.2f [m2/g] (super-micropore*1.5)" % (ndfds[len(ndfds)-1,4]+supermicropore_s*0.5))
print("***************************************************************************************************")
#
text  = "***************************************************************************************************\n"
text += "NLDFT (carbon slit model), DES) \n"
text += "\n"
text += "specific surface area and volume\n"
text += "ultra-micropore: "+"{:.2f}".format(ultramicropore_s)+" [m2/g], "+"{:.2f}".format(ultramicropore_v)+" [cm3/g] (w < 0.7 nm) \n"
text += "super-micropore: "+"{:.2f}".format(supermicropore_s)+" [m2/g], "+"{:.2f}".format(supermicropore_v)+" [cm3/g] (0.7 =< w < 2.0 nm) \n"
text += "micropore:       "+"{:.2f}".format(micropore_s)+" [m2/g], "+"{:.2f}".format(micropore_v)+" [cm3/g] Attention!!! limited range (2-10 nm) \n"
text += "total ds, V:    "+"{:.2f}".format(ndfds[len(ndfds)-1,4])+" [m2/g], "+"{:.2f}".format(ndfds[len(ndfds)-1,2])+" [cm3/g] Attention!!! limited range (0.4 =< w =< 10 nm) \n"
text += "************************************************\n"
text += "Note \n"
text += "The BET method underestimates the specific surface area of ultra-micropore region. \n"
text += "The BET method overestimates the specific surface area of super-micropore region by up to 50%. \n"
text += "Since the BET model assumes multi-layer adsorption, it holds only for pores larger than mesopores. In addition, the pore surface area tends to be overestimated because the interaction from the solid surface acting on the second and subsequent layers is ignored. \n"
text += "total ds: "+"{:.2f}".format(ndfds[len(ndfds)-1,4]+supermicropore_s*0.5)+" [m2/g] (super-micropore*1.5) \n"
text += "***************************************************************************************************\n"
fileobj = open("./plot/info_des.txt",'w')
fileobj.write(text)
#
x = ndfds[:,0]
y = ndfds[:,3]
y2 = ndfds[:,4]
#
def minor_tick(x, pos):
    if x >= 2:
        return f"{x:.0f}"
    elif not x % 1.0:
        return " "
    return f"{x:.1f}"
#
fig = plt.figure(figsize=(15,8))
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()
ax1.plot(x, y, label="Incremental Surface Area", color='black')
ax1.set_ylabel('Incremental Surface Area $(m^{2}/g)$', fontsize=18, fontname='Arial')
ax1.set_xscale("log")
ax1.set_xlabel("Pore size (nm)", fontsize=18, fontname='Arial')
ax1.grid()
#ax1.axvline(x=1, ymin=0, ymax=1.0, color='gray', lw=1, ls='-', alpha=0.6)
#ax1.axvline(x=10, ymin=0, ymax=1.0, color='gray', lw=1, ls='-', alpha=0.6)
ax1.set_xticks([1, 10])
ax1.set_xticklabels(["1", "10"])
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_minor_formatter(minor_tick)
ax1.tick_params(which='minor', width=1.0, labelsize=18)
ax2.plot(x, y2, label="Cumulative Surface Area", color='red', linestyle="--")
ax2.set_ylabel('Cumulative Surface Area $(m^{2}/g)$', fontsize=18, fontname='Arial') 
#ax2.tick_params(labelsize=18)
#
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='center right')
#
plt.title("PSD plot NLDFT (carbon slit), DES", fontsize=18, fontname='Arial')
fig.savefig('./plot/NLDFT_deltaS_DES.jpg')
plt.show()

# set name of columns
ndf = pd.DataFrame(ndfds)
ndf.columns = ['pore_widths_nm', 'pore_distribution', 'pore_volume_cumulative_cm^3g^-1', 'ds_m^2g^-1', 'cumulative_ds']

# output window and excel file
#import pprint
#pprint.pprint(ndf)
ndf.to_csv("./plot/result_dft_des.csv", index=False)