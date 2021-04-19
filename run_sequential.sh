#!/bin/bash

rm -r plot_sequential
mkdir plot_sequential
#
for file in ./sequential_data/*.csv; do
  rm -r plot
  mkdir plot
  cp $file case.csv
  file_name=`basename $file .csv`
  echo ${file_name}
  ./run.sh
  cp -r plot ./plot_sequential/${file_name}
  cp $file ./plot_sequential/${file_name}/${file_name}.csv
  cp case.csv ./plot_sequential/${file_name}/case.csv
  #diff -y case.csv ${file_name}.csv
done
#
rm -r plot
mkdir plot

