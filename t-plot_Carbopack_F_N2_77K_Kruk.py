import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

def idx_of_the_nearest(data, value):
    idx = np.argmin(np.abs(np.array(data) - value))
    return idx

dfs = pd.read_csv("./convert_PP0_to_alpha-s/carbon_additional_data/Carbopack_F_N2_77K_convert_data.txt", header = 0)
#print(dfs.iloc[:,0])
#print(dfs.iloc[:,1])

pp0_standard = []
t_standard = []
x= 0
for header1 in dfs.iloc[:,0]:
  if dfs.iloc[x,0][0] == "#":
    pass
  else:
    pp0_standard.append(float(dfs.iloc[x,0]))
    t_standard.append(float(dfs.iloc[x,3]))
  x = x + 1

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

df = pd.read_csv("case.csv", header = 0)
#print(df.iloc[:,0])
#print(df.iloc[:,1])

pp0_obserbed = []
cm3STP_obserbed = []
flag = 0
x= 0
for header1 in df.iloc[:,0]:
  if flag == 1:
    if float(df.iloc[x,0]) >= pp0max or (float(df.iloc[x+1,0]) - float(df.iloc[x,0])) < 0:
      flag = 2
    elif float(df.iloc[x,0]) <= pp0min:
      pass
    else:
      pp0_obserbed.append(float(df.iloc[x,0]))
      cm3STP_obserbed.append(float(df.iloc[x,1]))
  if df.iloc[x,0] == "pressure":
    flag = 1
  x = x + 1

#print(pp0_obserbed)
#print(cm3STP_obserbed)
#pp0_obserbed = df.iloc[:,0]
#cm3STP_obserbed = df.iloc[:,1]
#cm3STP_max = max(df.iloc[:,1])*1.1
cm3STP_max = max(cm3STP_obserbed)*1.1
#plt.scatter(pp0_obserbed, cm3STP_obserbed, label="obserbed (ads)")
#plt.show()

method = interpolate.interp1d
fitted_curve = method(pp0_standard, t_standard)
t_obserbed = fitted_curve(pp0_obserbed)

index = idx_of_the_nearest(t_obserbed, 0.354)
#print(index)
#print(df.iloc[index,1])
x = np.linspace(0, max(t_obserbed), 100)
#y = df.iloc[index,1]*2 * x
#s = df.iloc[index,1]*2 * 2.332581 * 0.599642483
#print(cm3STP_obserbed[index])
#y = cm3STP_obserbed[index]*2 * x
#s = cm3STP_obserbed[index]*2 * 2.332581 * 0.599642483
slope = ((cm3STP_obserbed[index+1]-cm3STP_obserbed[index])/(t_obserbed[index+1]-t_obserbed[index])*(0.354-t_obserbed[index])+cm3STP_obserbed[index])/0.354
y = slope * x
s = slope * 2.332581 * 0.599642483
x_max = max(x)

plt.plot(t_obserbed, cm3STP_obserbed, c="red", label="obserbed (ads)")
plt.plot(x, y, c="blue", label="fitted: "+'{:.1f}'.format(s)+" [$m^{{2}}/g$]", linestyle="dashed")
plt.axvline(x=0.354, c="gray", label="limit", linestyle="dashed")
plt.xlabel('t [nm]')
plt.ylabel('$cm^{{3}}STP/g$')
plt.xlim(0, x_max)
plt.ylim(0, cm3STP_max)
plt.legend()
plt.title('t-plot')
plt.show()

print("Surface area (of t-plot): "+'{:.1f}'.format(s)+" [m2/g]")
