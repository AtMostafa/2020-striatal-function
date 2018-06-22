To run those notebooks:

### 1) Either:
  - use only Python3
  - install a python3 kernel/environment with the code bellow, and stay in "python3" environment for the other 2 steps
  
---------------------------------------- 
conda create -n python3 python=3
source activate python3
conda install notebook ipykernel
sudo ipython kernel install
-----------------------------------------  
Type yes/Enter, and type root password for last line

### 2) Install latest phy (with Python3, or in python3 environment)

If phy was already install, remove folder ~/phy
Then in a terminal:
--------------------------------------------
conda install conda python=3.4 pip numpy matplotlib scipy h5py pyqt ipython-notebook requests six --yes
conda install -c kwikteam klustakwik2 --yes
pip install vispy
git clone git://github.com/kwikteam/phy.git ~/phy && cd ~/phy && python setup.py develop
----------------------------------------------


### 3) Other dependencies (with Python3, or in python3 environment)

If you have an error "No module named 'XXX'", type in a terminal:
    conda install XXX
and if it doesnt' work:
    pip install XXX

Here's all the module needed:

 - os, glob, pickle, datetime, collections, warnings  (built in, no need to install)
 - xmltodict     (pip install xmltodict)
 - numpy         (conda install numpy) 
 - pandas        (conda install pandas)
 - scipy         (conda install scipy)
 - six           (conda install six)
 - matplotlib    (conda install matplotlib)
 - h5py          (conda install h5py)
 
Usually you will need:
------------------------------------
pip install xmltodict
conda install pandas
------------------------------------
 
 
### NB

You don't need to do "source activate python3" before launching the notebook
  When you openned a notebook, check on the top right that it's written "Python 3"
  If it's "Python2", go in Kernel->Change Kernel -> Python3
  


 
 
