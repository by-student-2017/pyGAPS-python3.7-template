import csv

file = open("new_case.csv","w")
read_data_on = 0
num_values = []
with open("case.csv") as f:
  for row in csv.reader(f):
    if read_data_on == 1:
      num_values.append(row)
      if float(num_values[len(num_values)-1][0]) > 0.1:
        read_data_on = 0
    if 'pressure' in row:
      read_data_on = 1
    nlines = ", ".join(row)+"\n"
    file.write(nlines)
last_data = []
last_data.append(row)

for i in range(len(num_values)-1,-1,-1):
  if float(num_values[i][0]) < (float(last_data[len(last_data)-1][0]))*0.975:
    nlines = num_values[i][0]+","+num_values[i][1]+"\n"
    print(nlines)
    file.write(nlines)
