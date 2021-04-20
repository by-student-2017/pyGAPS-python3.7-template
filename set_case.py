import csv

file = open("new_case.csv","w")
read_data_on = 0
num_values = []
last_data = []
with open("case.csv") as f:
  for row in csv.reader(f):
    if row and str(row[0]) != "":
      if read_data_on == 1:
        num_values.append(row)
        if float(num_values[len(num_values)-1][0]) > 0.1:
          read_data_on = 2
      if ('pressure' in row) or ('pressure,loading' in row):
        read_data_on = 1
      nlines = ",".join(row)+"\n"
      file.write(nlines)
      last_data = row

for i in range(len(num_values)-1,-1,-1):
  if float(num_values[i][0]) < (float(last_data[0]))*0.975:
    nlines = num_values[i][0]+","+num_values[i][1]+"\n"
    print(nlines)
    file.write(nlines)
