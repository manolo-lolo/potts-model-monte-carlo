# Potts model Monte Carlo simulation
Simulation of the Potts model for a university course in Monte Carlo simulations


## Install dependencies
You need need Python3 with Tkinter and PIP.
On Ubuntu 18.04, you can get them by typing (with sudo rights):

```bash
apt install python3 python3-tk python3-pip python3-dev 
```

Create a virtual environment to install the packages dependencies and 
Poetry dependency manager:
```bash
python3 -m venv potts-venv
source potts-venv/bin/activate
pip install poetry
```

Then use Poetry to install the necessary Python dependencies (via virtualenv and pip):
```bash
poetry install
``` 

## Run GUI of Potts simulation
With the virtual environment still activated (`source potts-venv/bin/activate`), call
```bash
python main.py
```
