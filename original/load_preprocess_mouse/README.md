To run those notebooks, you need

### 1. **Python 3.4** and **conda** (Annaconda or Miniconda). You can either:

   * use only Python3 (uninstall previous conda and reinstall the Python 3 version)
   * install a python3 kernel/environment with the code bellow, and stay in "python3" environment for the other 2 steps

        conda create -n python3 python=3
        source activate python3
        conda install notebook ipykernel
        sudo ipython kernel install  

### 2. The **latest phy**

  If phy was already install, go in ~/phy folder:

    git pull
    python setup.py develop

  If not, install the last version from github:

    conda install conda python=3.4 pip numpy matplotlib scipy h5py pyqt ipython-notebook requests six --yes
    conda install -c kwikteam klustakwik2 --yes
    pip install vispy
    git clone git://github.com/kwikteam/phy.git ~/phy && cd ~/phy && python setup.py develop

### 3. Other Python modules

If you have an error "No module named 'XXX'", type in a terminal:

    conda install XXX

and if it doesn't work:

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

    pip install xmltodict
    conda install pandas
 
 
NB

When using an environment, you don't need to do "source activate python3" before launching the notebook.
When you opened a notebook, check on the top right that it's written "Python 3". If it's "Python2", go in Kernel->Change Kernel -> Python3