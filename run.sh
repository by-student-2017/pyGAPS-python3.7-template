#!/bin/bash

sed -i s/plt.show/#plt.show/g *.py
#python3 analysis.py | tee ./plot/info.txt
#
echo "==================================================================================================="
echo "NLDFT, ADS"
echo " "
python3 dft_fit_csv_ads.py
rm -f ./plot/info_ads.txt
#
echo "==================================================================================================="
echo "NLDFT, DES"
echo " "
python3 dft_fit_csv_des.py
rm -f ./plot/info_des.txt
#
#echo "==================================================================================================="
#echo "PSD"
#echo " "
python3 PSD-plot_pygaps_v202.py
#
echo "==================================================================================================="
echo "BET plot"
echo " "
python3 BET-plot.py
#
echo "==================================================================================================="
echo "Langmuir plot"
echo " "
python3 Langmuir-plot.py
#
echo "==================================================================================================="
echo "t plot Ref_CarbonBlack"
echo " "
#python3 t-plot_Ref_CarbonBlack.py
python3 t-plot_NGCB_N2_77K_Nakai.py
python3 t-plot_GCB-I_N2_77K_Nakai.py
#
echo "==================================================================================================="
echo "alpha-s plot"
echo " "
#python3 alpha-s-plot.py
python3 alpha-s-plot_CB_N2_77K_kaneko.py
python3 alpha-s-plot_NGCB_N2_77K_Nakai.py
python3 alpha-s-plot_GCB-I_N2_77K_Nakai.py
#
#echo "==================================================================================================="
#echo "DH plot"
#echo " "
python3 DH-plot.py
#
echo "==================================================================================================="
echo "DR plot"
echo " "
python3 DR-plot.py
#
echo "==================================================================================================="
echo "DA plot"
echo " "
python3 DA-plot.py
#
echo "==================================================================================================="
#
sed -i s/#plt.show/plt.show/g *.py

