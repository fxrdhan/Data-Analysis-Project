# Data Analytics Project

This repository contains a data analytics project analyzing public e-commerce data and a Streamlit dashboard.

## Table of Contents

- **[Project Structure](#project-structure)**
- **[Prerequisites](#prerequisites)**
- **[Setup Instructions](#setup-instructions)**
  - [Clone the Repository](#clone-the-repository)
  - [Python Environment Setup](#python-environment-setup)
  - [Virtual Environment Setup](#virtual-environment-setup)
  - [Install Dependencies](#install-dependencies)
  - [Running the Dashboard](#running-the-dashboard)
- **[Troubleshooting](#troubleshooting)**
  - [Common Issues and Solutions](#common-issues-and-solutions)

## Project Structure

```bash
.
├── dashboard
│   ├── dashboard.py
│   ├── pngwing.com.png
├── e-commerce_public_dataset
│   ├── *.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
├── script.py
├── url.txt
└── visualization_output
    ├── *.png
```

## Prerequisites
- [Git](https://git-scm.com/downloads)
- [pyenv](https://github.com/pyenv/pyenv)
- Python3

## Setup Instructions

### Clone the Repository

Clone this repository to local machine.

```bash
git clone https://github.com/fxrdhan/Data-Analytics-Project.git
cd Data-Analytics-Project
```

### Python Environment Setup

#### Install pyenv (if not already installed)

Linux:
    
```bash
curl https://pyenv.run | bash
```
Windows: [Here](https://github.com/pyenv-win/pyenv-win)

macOS: [Here](https://github.com/pyenv/pyenv?tab=readme-ov-file#homebrew-in-macos)
   
#### Set up shell environment for Pyenv
[Here](https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv)

#### Install Python3 version
[Here](https://github.com/pyenv/pyenv?tab=readme-ov-file#install-additional-python-versions)

### Virtual Environment Setup

Create and activate a virtual environment:

#### Create virtual environment
   
 - macOS/Linux:

   ```bash
   pyenv virtualenv 3.x.x myenv
   ```

 - Windows (PowerShell):
   
   ```powershell
   pyenv-win virtualenv 3.x.x myenv
   ```

#### Activate virtual environment

- macOS/Linux:

  ```bash
  pyenv activate myenv
  ```

- Windows (PowerShell):
  
  ```powershell
  pyenv shell myenv
  ```

#### To deactivate when you're done

- macOS/Linux:
  
  ```bash
  pyenv deactivate
  ```

- Windows (PowerShell):

  ```powershell
  pyenv shell system
  ```

### Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

## Troubleshooting

### Common Issues and Solutions

1. **pyenv: command not found**

   - Ensure pyenv is properly installed
   - Check if pyenv is added to your PATH
   - Restart your terminal
2. **Package installation errors**

   - Upgrade pip: `pip install --upgrade pip`
   - Try installing packages individually
3. **Streamlit port already in use**

   - Kill the process using the port: `lsof -i:8501`
   - Try running on a different port: `streamlit run dashboard.py --server.port XXXX`
