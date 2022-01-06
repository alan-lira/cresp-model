@echo off
:: Run with administrator privilegies
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )
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
:: Install 'Chocolatey' software manager
powershell Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
:: Install 'Vim' text editor
choco install vim -y

