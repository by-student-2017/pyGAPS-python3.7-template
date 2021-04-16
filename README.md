# pyGAPS-python3.7-template


## Install
1. cd ~
2. sudo apt update
3. sudo apt -y install python3-pip
4. pip3 install pygaps==2.0.2
5. git clone https://github.com/by-student-2017/pyGAPS-python3.7-template.git
6. cd ~/pyGAPS-python3.7-template
7.  chmod +x run.sh


## Usage -1-
1. cd ~/pyGAPS-python3.7-template
2. python3 dft_fit_csv_des.py
3. (see plot directory)
4. (write your data on case.csv, please.)


## Usage -2-
1. cd ~/pyGAPS-python3.7-template
2. ./run.sh | tee ./plot/info.txt
3. (see plot directory)
4. (write your data on case.csv, please.)


## Ubuntu 20.04 LTS (WSL version case)
1. sudo apt install x11-apps
2. echo 'export DISPLAY=localhost:0.0' >> ~/.bashrc
3. source ~/.bashrc
4. sudo apt -y install python3-tk
5. (plase install XLaunch)


Maybe, PSD-plot_pygaps_v303.py is for python 3.9.