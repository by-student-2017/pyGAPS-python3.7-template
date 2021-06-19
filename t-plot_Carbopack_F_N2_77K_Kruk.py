import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np


# ********** Setting the magnification of MP data **********
times = 100.0
# ***************************************


# ********** define function to find index of nearest **********
def idx_of_the_nearest(data, value):
    idx = np.argmin(np.abs(np.array(data) - value))
    return idx
# ***************************************


# ********** get standard data **********
dfs = pd.read_csv("./convert_PP0_to_alpha-s/carbon_additional_data/Carbopack_F_N2_77K_convert_data.txt", header = 0)
#print(dfs.iloc[:,0])
#print(dfs.iloc[:,1])

pp0_standard = []
t_standard = []
tx= 0
for header1 in dfs.iloc[:,0]:
  if dfs.iloc[tx,0][0] == "#":
    pass
  else:
    pp0_standard.append(float(dfs.iloc[tx,0]))
    t_standard.append(float(dfs.iloc[tx,3]))
  tx = tx + 1
# ***************************************


# ********** check standard data ********** 
#print(pp0_standard)
#print(t_standard)
#pp0_standard = dfs.iloc[:,0]
#t_standard = dfs.iloc[:,1]
#t_max = max(dfs.iloc[:,1])
pp0min = min(pp0_standard)
pp0max = max(pp0_standard)
#t_max = max(t_standard)
#plt.scatter(pp0_standard, t_standard, label="standard")
#plt.show()
# ***************************************


# ********** get sample data ********** 
df = pd.read_csv("case.csv", header = 0)
#print(df.iloc[:,0])
#print(df.iloc[:,1])

pp0_obserbed = []
cm3STP_obserbed = []
flag = 0
ox= 0
for header1 in df.iloc[:,0]:
  if flag == 1:
    if float(df.iloc[ox,0]) >= pp0max or (float(df.iloc[ox+1,0]) - float(df.iloc[ox,0])) < 0:
      flag = 2
    elif float(df.iloc[ox,0]) <= pp0min:
      pass
    else:
      pp0_obserbed.append(float(df.iloc[ox,0]))
      cm3STP_obserbed.append(float(df.iloc[ox,1]))
  if df.iloc[ox,0] == "pressure":
    flag = 1
  ox = ox + 1
# ***************************************


# ********** check sample data ********** 
#print(pp0_obserbed)
#print(cm3STP_obserbed)
#pp0_obserbed = df.iloc[:,0]
#cm3STP_obserbed = df.iloc[:,1]
#cm3STP_max = max(df.iloc[:,1])*1.1
cm3STP_max = max(cm3STP_obserbed)*1.1
#plt.scatter(pp0_obserbed, cm3STP_obserbed, label="obserbed (ads)")
#plt.show()
# ***************************************


# ********** interpolation with standard data
method = interpolate.interp1d
fitted_curve = method(pp0_standard, t_standard)
t_obserbed = fitted_curve(pp0_obserbed)
# ***************************************


# ********** calculate slope from raw data ********** 
index = idx_of_the_nearest(t_obserbed, 0.354)
#print(index)
#print(df.iloc[index,1])
fx = np.linspace(0, max(t_obserbed), 100)
#y = df.iloc[index,1]*2 * fx
#s = df.iloc[index,1]*2 * 2.332581 * 0.599642483/1.0
#print(cm3STP_obserbed[index])
#y = cm3STP_obserbed[index]*2 * fx
#s = cm3STP_obserbed[index]*2 * 2.332581 * 0.599642483/1.0
slope = ((cm3STP_obserbed[index+1]-cm3STP_obserbed[index])/(t_obserbed[index+1]-t_obserbed[index])*(0.354-t_obserbed[index])+cm3STP_obserbed[index])/0.354
fy = slope * fx
fs = slope * 2.332581 * 0.599642483/1.0
fx_max = max(fx)
# ***************************************


# ********** cut raw data ********** 
t_index = idx_of_the_nearest(t_obserbed, 0.3)
low_cut_t_obserbed = []
low_cut_cm3STP_obserbed = []
flag = 0
tx= 0
for header1 in cm3STP_obserbed:
  if tx == t_index:
    flag = 1
  if flag == 1:
    low_cut_t_obserbed.append(t_obserbed[tx])
    low_cut_cm3STP_obserbed.append(cm3STP_obserbed[tx])
  tx = tx + 1
#print(low_cut_t_obserbed)
#print(low_cut_cm3STP_obserbed)
# ***************************************


# ********** interpolation by Scipy ********** 
#i_method = lambda x, y: interpolate.interp1d(x, y, kind="cubic")
i_method = interpolate.Akima1DInterpolator
t_fitted_curve = i_method(low_cut_t_obserbed, low_cut_cm3STP_obserbed)
tx = np.arange(min(t_obserbed)+0.151, max(t_obserbed)-0.01, 0.005)
t_fitted_data = t_fitted_curve(tx)
# ***************************************


# ********** differential for MP method ********** 
d_t_fitted_data = []
dtx = []
for dx in range(1,len(t_fitted_data)):
    sur = (t_fitted_data[dx]-t_fitted_data[dx-1])/0.01*2.332581*0.599642483/1.0
    d_t_fitted_data.append(sur)
    dtx.append(tx[dx-1])
# ***************************************


# ********** delta volume from MP method ********** 
b_t_fitted_data = []
btx = []
dt_old = 0.0
for bx in range(1,len(t_fitted_data)):
  if tx[bx] >= 0.354:
    dt = (t_fitted_data[bx]-t_fitted_data[bx-1])/(tx[bx]-tx[bx-1])
    #print (t_fitted_data[bx]-dt*tx[bx])
    dvol = (t_fitted_data[bx]-dt*tx[bx]) - (t_fitted_data[bx-1]-dt_old*tx[bx-1])
    #print (vol)
    if dvol <= 0.0:
      dvol = 0.0
    b_t_fitted_data.append(dvol*times)
    btx.append(tx[bx])
    dt_old = dt
# ***************************************


# ********** delta surface area from MP method ********** 
dd_t_fitted_data = []
ddtx = []
for ddx in range(1,len(d_t_fitted_data)):
  if tx[ddx] >= 0.354:
    dsur = d_t_fitted_data[ddx-1]-d_t_fitted_data[ddx]
    dd_t_fitted_data.append(dsur*times)
    ddtx.append(tx[ddx])
# ***************************************


# ********** show graph **********
fig = plt.figure()
ax1 = fig.subplots()
ax2 = ax1.twinx()
#ax1.plot(x, y1) # sample 1
#ax2.plot(x, y2) # sample 2

ax1.plot(t_obserbed, cm3STP_obserbed, c="red", label="obserbed (ads)")
ax1.plot(fx, fy, c="blue", label="fitted: "+'{:.1f}'.format(fs)+" [$m^{{2}}/g$]", linestyle="dashed")
ax1.plot(tx, t_fitted_data, c="green", label="fitted_curve (ads)", linestyle="dashed")
ax1.plot(btx, b_t_fitted_data, c="black", label="MP method x "+str(times)+"\n (dV [$cm^{{3}}STP/g$])", linestyle="dashed")
ax1.axvline(x=0.354, c="gray", label="limit", linestyle="dashed")
ax2.plot(ddtx, dd_t_fitted_data, c="orange", label="MP method x "+str(times)+"\n (dS [$m^{{2}}/g$])", linestyle="dashed")

plt.title("t-plot and MP method")
plt.xlim(0, fx_max)
plt.xlabel('t [nm]')
ax1.set_ylim(0, cm3STP_max)
ax1.set_ylabel('V or dV [$cm^{{3}}STP/g$]')
ax2.set_ylim(0, cm3STP_max)
ax2.set_ylabel('dS [$m^{{2}}/g$]')
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='center right')
plt.show()
# ***************************************


# ********** show result **********
print("Surface area (of t-plot): "+'{:.1f}'.format(s)+" [m2/g]")
# ***************************************