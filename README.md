# Data Analytics Project

This repository contains a data analytics project analyzing public e-commerce data and a Streamlit dashboard.

## Menu

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Clone the Repository](#1-clone-the-repository)
  - [Python Environment Setup](#2-python-environment-setup)
  - [Virtual Environment Setup](#3-virtual-environment-setup)
  - [Install Dependencies](#4-install-dependencies)
  - [Running the Dashboard](#5-running-the-dashboard)
- [Troubleshooting](#troubleshooting)
  - [Common Issues and Solutions](#common-issues-and-solutions)

## Project Structure.

## Prerequisites

Before running this project, ensure you have the following installed:

- Git
- pyenv (for Python version management)
- Python 3.x.x

## Setup Instructions

### 1. Clone the Repository

Clone this repository to local machine.

```bash
git clone https://github.com/fxrdhan/Data-Analytics-Project.git
cd Data-Analytics-Project
```

### 2. Python Environment Setup

This project uses pyenv for Python version management. Follow these steps to set up the environment:

1. Install pyenv (if not already installed)

   Linux :

   ```bash
   curl https://pyenv.run | bash
   ```

   Windows:

   ```bash
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
   ```

   macOS (using Homebrew):

   ```bash
   brew install pyenv
   ```
2. Configure your shell environment:

   For macOS/Linux (bash), add to `~/.bashrc`, if use zsh add to `~/.zshrc`:

   ```txt
   export PYENV_ROOT="$HOME/.pyenv"
   command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init -)"
   ```

   For Windows, environment variables are automatically set by the installer.

   Restart your terminal for changes to take effect.
3. Install Python 3.x.x:

   List all available Python versions:

   ```bash
   pyenv install --list | grep " 3\."
   ```

   Install Python (choose the latest stable version):

   ```bash
   pyenv install 3.x.x
   ```

   Verify installation:

   ```bash
   python --version  # Should show your installed Python version
   ```
4. Set local Python version:

   ```bash
   pyenv local 3.x.x
   ```

### 3. Virtual Environment Setup

Create and activate a virtual environment:

1. Create virtual environment:

   ```bash
   python -m venv venv
   ```
2. Activate virtual environment:

   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### 4. Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

### 5. Running the Dashboard

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
