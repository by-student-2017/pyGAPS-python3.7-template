#!/bin/bash

sed -i s/plt.show/#plt.show/g *.py
python3 analysis.py | tee ./plot/info.txt
sed -i s/#plt.show/plt.show/g *.py

