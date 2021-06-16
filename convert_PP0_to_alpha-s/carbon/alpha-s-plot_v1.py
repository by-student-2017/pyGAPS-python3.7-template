import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

def idx_of_the_nearest(data, value):
    idx = np.argmin(np.abs(np.array(data) - value))
    return idx

dfs = pd.read_csv("Non-Graphitized_carbon_black_sample_NGCB_N2_77K_convert_data.txt", header = 5)
#print(dfs.iloc[:,0])
#print(dfs.iloc[:,1])
pp0_standard = dfs.iloc[:,0]
as_standard = dfs.iloc[:,1]
as_max = max(dfs.iloc[:,1])
#plt.scatter(pp0_standard, as_standard, label="standard")
#plt.show()

df = pd.read_csv("case._pp0_cm3STP.csv", header = 21)
#print(df.iloc[:,0])
#print(df.iloc[:,1])
pp0_obserbed = df.iloc[:,0]
cm3STP_obserbed = df.iloc[:,1]
cm3STP_max = max(df.iloc[:,1])*1.1
#plt.scatter(pp0_obserbed, cm3STP_obserbed, label="obserbed")
#plt.show()

method = interpolate.interp1d
fitted_curve = method(pp0_standard, as_standard)
as_obserbed = fitted_curve(pp0_obserbed)

index = idx_of_the_nearest(as_obserbed, 0.5)
#print(index)
#print(df.iloc[index,1])
x = np.linspace(0, max(as_obserbed), 100)
y = df.iloc[index,1]*2 * x
s = df.iloc[index,1]*2 * 2.715517

plt.plot(as_obserbed, cm3STP_obserbed, c="red", label="obserbed")
plt.plot(x, y, c="blue", label="fitted: "+'{:.1f}'.format(s)+" [$m^{{2}}/g$]", linestyle="dashed")
plt.axvline(x=0.5, c="gray", label="monolayer", linestyle="dashed")
plt.xlabel('alpha-s')
plt.ylabel('$cm^{{3}}STP/g$')
plt.xlim(0, as_max)
plt.ylim(0, cm3STP_max)
plt.legend()
plt.title('alpha-s plot')
plt.show()
