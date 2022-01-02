@echo off
:: Download 'get-pip.py' script file
powershell -Command "Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"
:: Install/Upgrade 'pip' package installer (from the get-pip.py downloaded script)
python get-pip.py
:: Delete 'get-pip.py' script file
del get-pip.py
:: Install/Upgrade 'NumPy' library
python -m pip install --upgrade numpy
:: Install/Upgrade 'SciPy' library
python -m pip install --upgrade scipy
:: Install/Upgrade 'GurobiPy' library
python -m pip install --upgrade gurobipy

