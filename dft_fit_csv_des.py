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
ultramicropore = 0.0
supermicropore = 0.0
micropore = 0.0
macropore = 0.0
#
ndfds[0,3] = (ndfds[0,2] - 0.0)/(ndfds[0,0]/2.0)*1000.0
ndfds[0,4] = ndfds[0,3]
for num in range(1,len(ndfds)):
  ndfds[num,3] = (ndfds[num,2] - ndfds[num-1,2])/(ndfds[num,0]/2.0)*1000.0
  ndfds[num,4] = ndfds[num-1,4] + ndfds[num,3]
  if (ndfds[num,0] < 0.7):    # < 0.7 nm: ultra-micropore
    ultramicropore = ultramicropore + ndfds[num,3]
  elif (ndfds[num,0] < 2.0):  # 0.7 - 2 nm: super-micropore
    supermicropore = supermicropore + ndfds[num,3]
  elif (ndfds[num,0] < 50.0): # 2 - 50 nm: micropore
    micropore = micropore + ndfds[num,3]
  else:                       # > 50 nm: macropore
    macropore = macropore + ndfds[num,3]
#
print("***************************************************************************************************")
print("pecific surface area")
print("ultra-micropore: %7.2f [m^2/g] (w < 0.7 nm)" % (ultramicropore))
print("super-micropore: %7.2f [m^2/g] (0.7 =< w < 2.0 nm)" % (supermicropore))
print("micropore: %7.2f [m^2/g], Attention!!! limited range (2-10 nm)" % (micropore))
print("total ds: %7.2f [m^2/g], Attention!!! limited range (0.4 =< w =< 10 nm)" % (ndfds[len(ndfds)-1,4]))
print("***************************************************************************************************")
print("Note")
print("The BET method underestimates the specific surface area of ultra-micropore region.")
print("The BET method overestimates the specific surface area of super-micropore region by up to 50%.")
print("Since the BET model assumes multi-layer adsorption, it holds only for pores larger than mesopores. In addition, the pore surface area tends to be overestimated because the interaction from the solid surface acting on the second and subsequent layers is ignored. ")
print("total ds: %7.2f [m^2/g] (super-micropore*1.5)" % (ndfds[len(ndfds)-1,4]+supermicropore*0.5))
print("***************************************************************************************************")
#
text  = "***************************************************************************************************\n"
text += "NLDFT (carbon slit model), DES) \n"
text += "\n"
text += "specific surface area \n"
text += "ultra-micropore: "+"{:.2f}".format(ultramicropore)+" [m^2/g] (w < 0.7 nm) \n"
text += "super-micropore: "+"{:.2f}".format(supermicropore)+" [m^2/g] (0.7 =< w < 2.0 nm) \n"
text += "micropore: "+"{:.2f}".format(micropore)+" [m^2/g], Attention!!! limited range (2-10 nm) \n"
text += "total ds: "+"{:.2f}".format(ndfds[len(ndfds)-1,4])+" [m^2/g], Attention!!! limited range (0.4 =< w =< 10 nm) \n"
text += "************************************************\n"
text += "Note \n"
text += "The BET method underestimates the specific surface area of ultra-micropore region. \n"
text += "The BET method overestimates the specific surface area of super-micropore region by up to 50%. \n"
text += "Since the BET model assumes multi-layer adsorption, it holds only for pores larger than mesopores. In addition, the pore surface area tends to be overestimated because the interaction from the solid surface acting on the second and subsequent layers is ignored. \n"
text += "total ds: "+"{:.2f}".format(ndfds[len(ndfds)-1,4]+supermicropore*0.5)+" [m^2/g] (super-micropore*1.5) \n"
text += "***************************************************************************************************\n"
fileobj = open("./plot/info_des.txt",'w')
fileobj.write(text)
#
x = ndfds[:,0]
y = ndfds[:,3]
y2 = ndfds[:,4]
#
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()
ax1.plot(x, y, label="ds", color='black')
ax1.set_xlabel("Pore size (nm)")
ax1.set_ylabel('Incremental Surface Area $(m^{2}/g)$')
ax2.plot(x, y2, label="Cumulative Surface Area", color='red', linestyle="--")
ax2.set_ylabel('Cumulative Surface Area $(m^{2}/g)$') 
#
plt.grid()
plt.title("PSD plot NLDFT (carbon slit), DES")
plt.xscale("log")
fig1 = plt.figure(1)
fig1.savefig('./plot/NLDFT_deltaS_DES.jpg')
plt.show()

# set name of columns
ndf = pd.DataFrame(ndfds)
ndf.columns = ['pore_widths_nm', 'pore_distribution', 'pore_volume_cumulative_cm^3g^-1', 'ds_m^2g^-1', 'cumulative_ds']

# output window and excel file
#import pprint
#pprint.pprint(ndf)
ndf.to_csv("./plot/result_dft_des.csv", index=False)