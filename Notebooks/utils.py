# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:32:51 2022

@author: admin
"""
# import sys
# print('Python', sys.version)

import pandas as pd
# print('pandas', pd.__version__)

# import matplotlib
import matplotlib.pyplot as plt
# print('matplotlib', matplotlib.__version__)

# import statsmodels
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# print('statsmodels', statsmodels.__version__)

import numpy as np
# print('numpy', np.__version__)

def collect_windows(df, target, size = 5): 
    cols = list(df.columns)
    cols.remove(target)
     # Creo una copia del dataset
    dft = df.copy()
    
    for col in cols:
    # Applico lag alle colonne
        for j in range(1,size+1):
            name = col + '_Lag_'+str(j)
            dft[name] = df[col].shift(j)
   
    dft[target] = df[target].shift(-7)
    
    
    dft.dropna(subset=list(dft.columns), inplace=True)
    
    return dft

# create a differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return diff
 
# invert differenced forecast
def inverse_difference(last_ob, value):
    return value + last_ob
# Apply inverse
def apply_inverse_diff(data, diff):
    return [inverse_difference(data[i], diff[i]) for i in range(len(diff))]

class print_plot(object):
    def __init__(self, df, colonna):
        
        self.df = df
        self.colonna = colonna
        
        # Semplice visualizzazione della serie
    def plot_series(self):
        plt.plot(self.df[self.colonna], linewidth = 2)

            # Labelling 

        plt.xlabel("Giorno")
        plt.ylabel(self.colonna)
        plt.title("Serie di " + self.colonna)
        
        plt.tight_layout()
        plt.tick_params(axis='x', rotation=90)
        
        plt.show()
    
    def plot_years_serie(self, n_anni):
            # Unico plot con piu' serie annuali
        serie_livello = list(self.df[self.colonna])
        for i in range(0,n_anni):
            n = i*365
            serie_anno = serie_livello[n:(n+365)]
            plt.plot(serie_anno, label='Anno_'+str(i+1), marker = 'o', markersize=3,
                         linewidth=1)

        plt.title('Confronto Annuale di ' + self.colonna)
        plt.ylabel(self.colonna)
        plt.xlabel('Giorno')
        
        plt.legend()

        plt.tight_layout()

        plt.show() 
    
# Boxplot Annuali
    def boxplot_annuali(self, anno_inizio, anno_fine):
        series = self.df[(self.df['Year']>=anno_inizio) & (self.df['Year']<=anno_fine)][['Data', self.colonna]]
        groups = series.groupby(pd.Grouper(key='Data', freq='Y'))
        years = pd.DataFrame()
        for name, group in groups:
            # Tutti di lunghezza 365
            years[name.year] = list(group[self.colonna])[:365]
        years.boxplot()
                
        plt.tight_layout()
        plt.tick_params(axis='x', rotation=90)
        plt.show()
        
    def plot_stazionario_varianza(self, gruppo):
        result = self.df.groupby([gruppo], as_index=False).agg(
                {self.colonna:['mean','std']})
        x = result[self.colonna]['mean']
        y = result[self.colonna]['std']
            
        # Regressione
        m, b = np.polyfit(x, y, 1)
        
        #Plot
        plt.plot(x, y, 'o')
        plt.plot(x, m*x + b)
    

   


