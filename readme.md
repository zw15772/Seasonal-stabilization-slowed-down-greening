# Readme

# 1. System requirements

## 1.1 Softwares and operating system

```bash
Windows 11 Pro 23H2
PyCharm Community Edition 2024.1
Jupyter notebook 7.0.7
Python 3.9.4
```

## 1.2 Python Dependencies

```bash
GDAL 3.4.0
h5py 3.6.0
matplotlib 3.5.1
netCDF4 1.5.8
numpy 1.20.3
pandas 1.3.2
pingouin 0.5.1
scikit-learn 0.24.2
scipy 1.7.1
seaborn 0.11.2
statsmodels 0.13.2
```

## 1.3 Any required non-standard hardware

None

# 2 Installation guide

## 2.1 Instructions

1. Download and install Miniforge Python installer

```bash
https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
```

1. Install the dependencies

```bash
conda install gdal, statsmodels, scikit-learn, pingouin, xycmap
```

1. Clone code

```bash
git clone https://github.com/zw15772/Seasonal-stabilization-slowed-down-greening.git
```

## 2.2 Typical install time on a "normal" desktop computer

5 minutes

# 3 Demo

## 3.1 Instructions to run on data

```bash
pip install notebook
jupyter notebook
```

## 3.2 Expected output

See expected output in ‘Core_algorithm.ipynb’ via jupyter notebook

## 3.3 Expected run time for demo on a "normal" desktop computer

Around 30 min

# 4 Instructions for use

## 4.1 How to run the software on your data

Prior to code execution, review the manuscript's Methods section to identify data pre-processing steps, such as early, peak, and late season extraction, z-score calculation, and time series de-trending.