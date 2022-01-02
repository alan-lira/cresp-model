# CRESP Model (cresp-model)
This is a simple Python implementation of the time cost model for MapReduce applications developed in the work entitled "CRESP: Towards Optimal Resource Provisioning for MapReduce Computing in Public Clouds". (https://ieeexplore.ieee.org/abstract/document/6678508/)

### 1. Installation (Linux / Windows Shell)

##### 1.1 Clone or download this repository's content:

###### *1.1.1 Clone (Requires [Git](https://git-scm.com/downloads "Download Git"))*

`$ git clone https://github.com/alan-lira/cresp-model.git`

###### *1.1.2 Download and extract (Linux Shell + Unzip)*

`$ sudo apt install unzip -y && wget -O cresp-model.zip https://github.com/alan-lira/cresp-model/archive/refs/heads/main.zip && unzip cresp-model.zip && mv cresp-model-main cresp-model && rm -rf cresp-model.zip`
###### *1.1.3 Download and extract (Windows Shell)*

`$ powershell -Command Invoke-WebRequest https://github.com/alan-lira/cresp-model/archive/refs/heads/main.zip -OutFile cresp-model.zip; Expand-Archive -Path cresp-model.zip; Move-Item -Path cresp-model\cresp-model-main -Destination .\; del cresp-model; Rename-Item cresp-model-main cresp-model; del cresp-model.zip`

##### 1.2 Install dependencies (Requires [Python](https://www.python.org/downloads/ "Download Python")):

###### *1.2.1 Linux Shell (Bash)*

`$ sh ./cresp-model/dependencies-installer/linux.sh`

###### *1.2.2 Windows Shell (Batch)*

`$ cresp-model\dependencies-installer\windows.cmd`

### 2. Basic Usage (Linux / Windows Shell)

*2.1 Navigate to "cresp-model" directory:*

> cd cresp-model


*2.2 Edit, as you wish, the input parameters and other settings on "cresp_config" file:*

> sudo apt install vim -y

> vim cresp_config

Tips for Vim users: Press "I" key to start editing; Press "Esc" key after edition; Type ":wq!" and then "Enter" to save the changes.

*2.3 Optimize the model with the desired input parameters:*

> python3 cresp_model.py