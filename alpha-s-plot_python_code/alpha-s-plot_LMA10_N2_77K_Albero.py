import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

as_coeff = 2.332581

def idx_of_the_nearest(data, value):
    idx = np.argmin(np.abs(np.array(data) - value))
    return idx

dfs = pd.read_csv("./convert_PP0_to_alpha-s/carbon/Carbon_LMA10_N2_77K_convert_data.txt", header = 0)
#print(dfs.iloc[:,0])
#print(dfs.iloc[:,1])

pp0_standard = []
as_standard = []
x= 0
for header1 in dfs.iloc[:,0]:
  if dfs.iloc[x,0][0] == "#":
    pass
  else:
    pp0_standard.append(float(dfs.iloc[x,0]))
    as_standard.append(float(dfs.iloc[x,1]))
  x = x + 1

pp0min = min(pp0_standard)
pp0max = max(pp0_standard)

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

cm3STP_max = max(cm3STP_obserbed)*1.1

method = interpolate.interp1d
fitted_curve = method(pp0_standard, as_standard)
as_obserbed = fitted_curve(pp0_obserbed)

index = idx_of_the_nearest(as_obserbed, 0.5)
#print(index)
#print(df.iloc[index,1])
x = np.linspace(0, max(as_obserbed), 100)
slope = ((cm3STP_obserbed[index+1]-cm3STP_obserbed[index])/(as_obserbed[index+1]-as_obserbed[index])*(0.5-as_obserbed[index])+cm3STP_obserbed[index])*2
y = slope * x
s = slope * as_coeff
x_max = max(x)

plt.plot(as_obserbed, cm3STP_obserbed, c="red", label="obserbed (ads)")
plt.plot(x, y, c="blue", label="fitted: "+'{:.1f}'.format(s)+" [$m^{{2}}/g$]", linestyle="dashed")
plt.axvline(x=0.5, c="gray", label="monolayer", linestyle="dashed")
plt.xlabel('alpha-s')
plt.ylabel('$cm^{{3}}STP/g$')
plt.xlim(0, x_max)
plt.ylim(0, cm3STP_max)
plt.legend()
plt.title('alpha-s plot')
plt.show()

plt.title("alpha-s-plot, ads", fontsize=18, fontname='Arial')
fig.savefig('./plot/alpha-s-plot.jpg')

print("***************************************************************************")
print("The current version only works with [P/P0 vs. cm3(STP)/g] data (case.csv)")
print("Surface area (of alpha-s plot): "+'{:.1f}'.format(s)+" [m2/g]")
print("***************************************************************************")

dft = pd.DataFrame([as_obserbed, cm3STP_obserbed])
dft.index = ['as', 'pore_volume[cm3(STP)/g]']
dft.T.to_csv("./plot/alpha-s-plot_results.csv")