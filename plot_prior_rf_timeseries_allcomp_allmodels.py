import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image

plt.rcParams['font.size'] = 5
plt.rcParams['figure.dpi'] = 300

model_list = {'CNRM1':'CNRM-CM6-1',
              'HadGEM3':'HadGEM3-GC31-LL',
              'NorESM2LM':'NorESM2'}


ens_list = {'CNRM1':np.arange(1,2,1),
            'HadGEM3':np.arange(1,2,1),
            'NorESM2MM': np.arange(1,2,1),
            'NorESM2LM': np.arange(1,2,1)} 


prior_nr = {'CNRM1':2,
            'HadGEM3':3 }






rf_list_org ={'Tot':'(a) Total',
              'antro':'(b) Anthropogenic',
              'Nat':'(c) Natural',
              'GHG':'(d) GHGs',
              'AER':'(e) Aerosols',
              'Rest':'(f) Rest',
              'LANDUSE':'(g) Landuse',
              'O3':'(h) Ozone'}

color_list = {'CNRM1':'darkblue',
              'HadGEM3':'darkgreen',
              'NorESM2MM':'darkred',
              'NorESM2LM':'orange'}



fig, axs = plt.subplots(nrows=4,ncols=2,figsize=(14/2.5,18/2.6))
 
for mod,model in enumerate(model_list):
    if model == 'NorESM2LM':
        rf_list = rf_list_org
    else:
        rf_list = dict(list(rf_list_org.items())[:-2])
        print(rf_list)
        
    axs=axs.flatten()

    for ens in ens_list[model]:
        scen = 'OutputAnalyse'+model+ 'R' + str(ens)
        for rf,rf_comp in enumerate(rf_list):
            filename = 'summary_rf_prior_timeseries_all_perc_'+rf_comp+scen+'.csv'

            print(filename)
            prior_rf=pd.read_csv('results_csv/'+filename,
                                index_col=0)
            
            axs[rf].plot(prior_rf['Median'],linewidth=0.5,color=color_list[model],label=model_list[model])
            axs[rf].fill_between(prior_rf.index, prior_rf['5perc'],
                                 prior_rf['95perc'],
                                 color=color_list[model],linewidth=0.25,
                                 alpha=0.3)
            axs[rf].set_title(rf_list[rf_comp], loc='left')
            axs[rf].set_ylabel('ERF [W m$^{-2}$]')

            axs[rf].legend()
            axs[rf].set_xlim([1850,2020])




            if rf_comp == 'Tot':
                print(model)
                print('Tot:')
                print('1950:')
                print(0.5*(prior_rf['95perc'].loc[1950]-prior_rf['5perc'].loc[1950]))
                print('2014:')
                print(0.5*(prior_rf['95perc'].loc[2010]-prior_rf['5perc'].loc[2010]))
            
#plt.suptitle('Prior')






    
plt.tight_layout()        

plt.savefig('Figures/ERFprior.png')

#plt.show()
