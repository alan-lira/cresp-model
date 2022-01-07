# _CRESP Model_ (cresp-model)
> This is a simple Python implementation of the time cost model for MapReduce applications developed in the work entitled "CRESP: Towards Optimal Resource Provisioning for MapReduce Computing in Public Clouds". (https://ieeexplore.ieee.org/abstract/document/6678508/)

## Supported Operating Systems

---
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Linux_logo.jpg/640px-Linux_logo.jpg" alt="drawing" title="Linux" height="48" width="42"/> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Windows_logo_-_2021.svg/800px-Windows_logo_-_2021.svg.png" alt="drawing" title="Windows" height="40" width="40"/>

## 1. Installation (Shell)

---

### 1.1 Clone OR download this repository's content.

##### 1.1.1 *Clone* [⚠️Requires [Git](https://git-scm.com/downloads "Download Git")]:

$ `git clone https://github.com/alan-lira/cresp-model.git`

**OR**

##### 1.1.2 *Download* and *extract*:

- **Linux**:

$ `sudo apt install unzip -y && wget -O cresp-model.zip https://github.com/alan-lira/cresp-model/archive/refs/heads/main.zip && unzip cresp-model.zip && mv cresp-model-main cresp-model && rm -rf cresp-model.zip`

- **Windows**:

$ `powershell -Command Invoke-WebRequest https://github.com/alan-lira/cresp-model/archive/refs/heads/main.zip -OutFile cresp-model.zip; Expand-Archive -Path cresp-model.zip; Move-Item -Path cresp-model\cresp-model-main -Destination .\; del cresp-model; Rename-Item cresp-model-main cresp-model; del cresp-model.zip`

### 1.2 Install dependencies [⚠️Requires [Python](https://www.python.org/downloads/ "Download Python")].

##### 1.2.1 Execute the <span style="color:SlateGray">*dependencies-installer*</span> script:

- **Linux (Bash)**:

$ `sh ./cresp-model/dependencies-installer/linux.sh`

- **Windows (Batch)**:

$ `.\cresp-model\dependencies-installer\windows.cmd`

> **NOTE**: The ***Vim*** text editor should be available after running the <span style="color:SlateGray">***dependencies-installer***</span> script suitable for your OS.
<br/><br/>
Vim basic commands example (keyboard key combination):
<br/><br/>
$ `vim example.txt`
<br/><br/>
🔹 `i`: Enables the edition mode;
<br/>
🔹 `Esc`: Disables the edition mode;
<br/>
🔹 `:` ➡ `w` ➡ `Enter`: Saves the changes made to target file;
<br/>
🔹 `:` ➡ `q` ➡ `Enter`: Quits the editor;
<br/>
🔹 `:` ➡ `w` ➡ `q` ➡ `!` ➡ `Enter`: Quits the editor, saving the changes made to target file;
<br/>
🔹 `:` ➡ `q` ➡ `!` ➡ `Enter`: Quits the editor, discarding the unsaved changes.

## 2. Basic Usage (Shell)

---

The usage consists of four interdependent major steps.

### 2.1 Generate a set of random settings for the *m* (Map slots), *r* (Reduce slots) and *M* (Map tasks) parameters.

##### 2.1.1 Edit <span style="color:DarkGoldenRod">*experiments_maker.cfg*</span>, considering the following fields:
🔸 <span style="color:Maroon">***number_of_experiments***</span>: Amount of {*m*, *r*, *M*} pseudorandom subset settings to be generated;
<br/>
🔸 <span style="color:Maroon">***data_block_size_in_megabytes***</span>: Size in Megabytes (MB) for each data block (e.g., 128 for Hadoop Distributed File System – HDFS);
<br/>
🔸 <span style="color:Maroon">***γ (gamma)***</span>: Amount of slots (cores) per node;
<br/>
🔸 <span style="color:Maroon">***experiments_output_file***</span>: Target output file path for experiments to be performed.
<br/>
🔸 <span style="color:Maroon">***m***</span>: Range for *m* pseudorandom values, where *m* ∈ N<sup>* </sup>;
<br/>
🔸 <span style="color:Maroon">***r***</span>: Range for *r* pseudorandom values, where *r* ∈ N<sup>* </sup>;
<br/>
🔸 <span style="color:Maroon">***M***</span>: Range for *M* pseudorandom values, where *M* ∈ N<sup>* </sup>.
<br/>
- **Linux**:
<br/>
$ `vim ./cresp-model/config/experiments_maker.cfg`
<br/><br/>
- **Windows**:
<br/>
$ `vim .\cresp-model\config\experiments_maker.cfg`

##### 2.1.2 Execute <span style="color:DarkBlue">*experiments_maker.py*</span> to generate the experiments file:
- **Linux**:
<br/>
$ `python3 ./cresp-model/experiments_maker.py`
<br/><br/>
- **Windows**:
<br/>
$ `python .\cresp-model\experiments_maker.py`

> **NOTE**: <span style="color:Maroon">***experiments_output_file***</span> will be auto generated from the fields set in <span style="color:DarkGoldenRod">***experiments_maker.cfg***</span>.

### 2.2 For each subset {*m*, *r*, *M*} formed, run the experiment and collect the execution time for a particular Map-Reduce application.

##### 2.2.1 Run each experiment defined in <span style="color:Maroon">*experiments_output_file*</span>, considering the following settings:

🔸 <span style="color:Maroon">***m***</span>: Number of Map slots;
<br/>
🔸 <span style="color:Maroon">***r***</span>: Number of Reduce slots;
<br/>
🔸 <span style="color:Maroon">***input_size_in_gb***</span>: Amount of input data in Gigabytes (GB);
<br/>
🔸 <span style="color:Maroon">***number_of_nodes***</span>: Amount of nodes to be used in the cluster;
<br/>
🔸 <span style="color:Maroon">***number_of_slots_per_node***</span>: Amount of available slots (*m* + *r*) per node in the cluster;
 <br/>
🔸 <span style="color:Maroon">***total_number_of_slots***</span>: Amount of available slots (*m* + *r*) in the cluster.

##### 2.2.2 Edit <span style="color:Maroon">*experiments_output_file*</span>, filing each <span style="color:Maroon">*execution_time_in_seconds*</span> field with the corresponding execution time observed:

- **Linux**:
<br/>
$ `vim ./cresp-model/experiments/experiments.txt`
<br/><br/>
- **Windows**:
<br/>
$ `vim .\cresp-model\experiments\experiments.txt`

### 2.3 From the experiments conducted, apply linear regression analysis (non-negative least squares – NNLS) to obtain the *β<sub>i</sub>* parameters.

##### 2.3.1 Edit <span style="color:DarkGoldenRod">*beta_parameters_learner.cfg*</span>, setting <span style="color:Maroon">*experiments_input_file*</span> field with the source file of experiments already performed:

- **Linux**:
<br/>
$ `vim ./cresp-model/config/beta_parameters_learner.cfg`
<br/><br/>
- **Windows**:
<br/>
$ `vim .\cresp-model\config\beta_parameters_learner.cfg`

##### 2.3.2 Execute <span style="color:DarkBlue">*beta_parameters_learner.py*</span> to calculate the *β<sub>i</sub>* parameters:
- **Linux**:
<br/>
$ `python3 ./cresp-model/beta_parameters_learner.py`
<br/><br/>
- **Windows**:
<br/>
$ `python .\cresp-model\beta_parameters_learner.py`

> **NOTE**: The <span style="color:Maroon">***β<sub>i</sub>***</span> fields of <span style="color:DarkGoldenRod">***cresp_optimizer.cfg***</span> will be auto updated with the *β<sub>i</sub>* parameters learned from <span style="color:Maroon">***experiments_input_file***</span>.

### 2.4 With the learned *β<sub>i</sub>* parameters, estimate the optimal *m* and *R* values that minimizes a particular optimization problem.  

##### 2.4.1 Edit <span style="color:DarkGoldenRod">*cresp_optimizer.cfg*</span>, considering the following fields:
🔸 <span style="color:Maroon">***β<sub>i</sub>***</span>: Beta parameters learned from the linear regression analysis (previous step);
<br/>
🔸 <span style="color:Maroon">***M***</span>: Number of Map tasks (chunks of input data, considering the data block size of a particular file system);
<br/>
🔸 <span style="color:Maroon">***γ (gamma)***</span>: Amount of slots (cores) per node;
<br/>
🔸 <span style="color:Maroon">***υ (upsilon)***</span>: Monetary cost (USD) of using a node for one hour;
<br/>
🔸 <span style="color:Maroon">***φ (phi)***</span>: Maximum monetary cost (USD) for finishing the job (budget constraint);
<br/>
🔸 <span style="color:Maroon">***τ (tau)***</span>: Maximum amount of time, in hours, for finishing the job (deadline constraint);
<br/>
🔸 <span style="color:Maroon">***m***</span>: Bounds associated to the *m* decision variable, where *m* ∈ N<sup>* </sup>;
<br/>
🔸 <span style="color:Maroon">***R***</span>: Bounds associated to the *R* decision variable, where *R* ∈ N<sup>* </sup>;
<br/>
🔸 <span style="color:Maroon">***optimization_problem***</span>: Problem to be optimized (Supported problems: 1, 2, 3): 1 – Given *φ*, find the best resource allocation to minimize the job time; 2 – Given *τ*, find the best resource allocation to minimize the monetary cost; 3 – Find the most economical solution for the job without *τ*;
<br/>
🔸 <span style="color:Maroon">***monetary_unit***</span>: Monetary cost solution output's unit (Supported units: USD);
<br/>
🔸 <span style="color:Maroon">***time_unit***</span>: Time cost solution output's unit (Supported units: second, minute, hour);
<br/>
🔸 <span style="color:Maroon">***optimization_modes***</span>: Optimization modes to be used (Supported modes: brute_force, gurobi).
<br/>
- **Linux**:
<br/>
$ `vim ./cresp-model/config/cresp_optimizer.cfg`
<br/><br/>
- **Windows**:
<br/>
$ `vim .\cresp-model\config\cresp_optimizer.cfg`

##### 2.4.2 Execute <span style="color:DarkBlue">*cresp_optimizer.py*</span> to estimate the optimal *m* and *R* values:
- **Linux**:
<br/>
$ `python3 ./cresp-model/cresp_optimizer.py`
<br/><br/>
- **Windows**:
<br/>
$ `python .\cresp-model\cresp_optimizer.py`

