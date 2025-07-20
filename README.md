# Affordable Multispectral Microscope (MSM) Dataset

This repository contains the dataset and related scripts for the development of an affordable multispectral microscope (MSM).

## Overview

The MSM project aims to provide a cost-effective, real-time multispectral imaging system for tissue analysis in pathology and biomedical research. The dataset supports research and development for intelligent multispectral imaging using standard brightfield microscopes, machine vision cameras, and single-board computers.

## Features

- Multispectral image data for tissue classification and analysis
- Ready-to-use Jupyter Notebooks for data exploration and modeling
- Python scripts for preprocessing, analysis, and visualization
- Instructions for setting up the MSM hardware and software environment

## Requirements

- Python 3.7 or higher
- [conda](https://docs.conda.io/en/latest/)
- All required packages listed in `environment.yml`
- Jupyter Notebook
- (Optional) Raspberry Pi for hardware integration

To install dependencies:
```bash
conda env create -f environment.yml
conda activate msm-env
