import matplotlib
def set_rc_params(**kwarg):
    matplotlib.rcParams['xtick.major.pad'] = 1
    matplotlib.rcParams['ytick.major.pad'] = 1
    matplotlib.rcParams['axes.labelpad']   = 2
    matplotlib.rcParams['axes.titlepad']   = 3
    
    
    for key,val in kwarg.items():
        matplotlib.rcParams[key] = val
