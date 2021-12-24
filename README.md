# CRESP Model (cresp-model)
This is a simple Python implementation of the time cost model for MapReduce applications developed in the work entitled "CRESP: Towards Optimal Resource Provisioning for MapReduce Computing in Public Clouds". (https://ieeexplore.ieee.org/abstract/document/6678508/)

### 1. Installation (Linux Terminal)

*1.1 Install pip:*
> sudo apt install python3-pip -y

*1.2 Install Gurobi Optimizer for Python (gurobipy):*
> python -m pip install gurobipy

*1.3 Clone or download this repository's content:*

*1.3.1 (Clone)*

> sudo apt install git -y

> git clone https://github.com/alan-lira/cresp-model.git

*1.3.2 (Download and Extract)*

> sudo apt install unzip -y

> wget https://github.com/alan-lira/cresp-model/archive/refs/heads/main.zip

> unzip main.zip

### 2. Usage (Linux Terminal)

*2.1 Navigate to "cresp-model" directory:*

> cd cresp-model


*2.2 Edit, as you wish, the input parameters and other settings on "cresp_config" file:*

> sudo apt install vim -y

> vim cresp_config

Tips for Vim users: Press "I" key to start editing; Press "Esc" key after edition; Type ":wq!" and then "Enter" to save the changes.

*2.3 Optimize the model with the desired input parameters:*

> python3 cresp_model.py