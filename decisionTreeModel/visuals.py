###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
#
# Display inline matplotlib plots with IPython
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
###########################################

import matplotlib.pyplot as pl
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from time import time
from sklearn.metrics import f1_score, accuracy_score

def feature_plot(importances, X_train, y_train):
    
    # Display the five most important features
    indices = np.argsort(importances)[::-1]
    columns = X_train.columns.values[indices[:5]]
    values = importances[indices][:5]

    # Creat the plot
    fig = pl.figure(figsize = (9,5))
    pl.title("Normalized Weights for First Five Most Predictive Features", fontsize = 16)
    rects = pl.bar(np.arange(5), values, width = 0.6, align="center", color = '#00A000', \
                label = "Feature Weight")
    
    # make bar chart higher to fit the text label
    axes = pl.gca()
    axes.set_ylim([0, np.max(values) * 1.1])

    # add text label on each bar
    delta = np.max(values) * 0.02
    
    for rect in rects:
        height = rect.get_height()
        pl.text(rect.get_x() + rect.get_width()/2., 
                height + delta, 
                '%.2f' % height,
                ha='center', 
                va='bottom')
    
    # Detect if xlabels are too long
    rotation = 0 
    for i in columns:
        if len(i) > 20: 
            rotation = 10 # If one is longer than 20 than rotate 10 degrees 
            break
    pl.xticks(np.arange(5), columns, rotation = rotation)
    pl.xlim((-0.5, 4.5))
    pl.ylabel("Weight", fontsize = 12)
    pl.xlabel("Feature", fontsize = 12)
    
    pl.legend(loc = 'upper center')
    pl.tight_layout()
    pl.show() 
