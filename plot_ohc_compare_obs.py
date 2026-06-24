import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


plt.rcParams['font.size'] = 4
plt.rcParams['figure.dpi'] = 300


model_list = [ 'CNRM1','HadGEM3','NorESM2LM','NorESM2MM']

#model_list = ['CNRM1']

ens_list = {'CNRM1':np.arange(1,31,1),
            'HadGEM3':np.arange(1,5,1),
            'NorESM2MM': np.arange(1,4,1),
            'NorESM2LM': np.arange(1,4,1)}


### Add "observations":
model_org = {'CNRM1':'CNRM-CM6-1',
             'HadGEM3':'HadGEM3-GC31-LL',
             'NorESM2LM':'NorESM2-LM',
             'NorESM2MM':'NorESM2-MM'}

ens_name = {'CNRM1':'i1p1f2',
            'HadGEM3': 'i1p1f3',
            'NorESM2LM':'i1p1f1',
            'NorESM2MM':'i1p1f1'}

color_list = {'CNRM1':'tab:blue',
              'HadGEM3':'tab:green',   
              'NorESM2MM':'tab:purple',
              'NorESM2LM':'tab:orange'}





fig, axes = plt.subplots(nrows=3, ncols=1,figsize=(14/3.5,19/3.5))
for model in model_list:

    
    for ens in ens_list[model]:
    
        file_cmip = 'ohc_700_bot_'+model_org[model]+ '_r'+str(ens)+'.csv'
        cmip_700_bot = pd.read_csv('observations/OHC/'+file_cmip,index_col=0)
        file_cmip = 'ohc_0_700_'+model_org[model]+ '_r'+str(ens)+'.csv'
        cmip_0_700 = pd.read_csv('observations/OHC/'+file_cmip,index_col=0)


        if ens == 1:
            axes[0].plot(cmip_0_700,linewidth = 0.5,linestyle='-', color=color_list[model], label=model_org[model])
            axes[1].plot(cmip_700_bot,linewidth = 0.5,linestyle='-',color=color_list[model], label=model_org[model])
            axes[2].plot(cmip_0_700+cmip_700_bot,linewidth = 0.5,linestyle='-',color=color_list[model], label=model_org[model])
        else:
            axes[0].plot(cmip_0_700,linewidth = 0.5,linestyle='-', color=color_list[model])
            axes[1].plot(cmip_700_bot,linewidth = 0.5,linestyle='-',color=color_list[model])
            axes[2].plot(cmip_0_700+cmip_700_bot,linewidth = 0.5,linestyle='-',color=color_list[model])
            
axes[0].set_title('(a) OHC 0-700 meters', loc = 'left')
axes[1].set_title('(b) OHC below 700 meters',loc='left')
axes[2].set_title('(c) OHC total',loc='left')


axes[0].set_ylabel('OHC [10$^{22}$ Joule] (relative to 2005 to 2014)')
axes[1].set_ylabel('OHC [10$^{22}$ Joule] (relative to 2005 to 2014)')
axes[2].set_ylabel('OHC [10$^{22}$ Joule] (relative to 2005 to 2014)')

axes[0].set_ylim([-30,12])
axes[1].set_ylim([-30,12])
axes[2].set_ylim([-30,12])
    
axes[0].set_xlim([1950,2015])
axes[1].set_xlim([1950,2015])
axes[2].set_xlim([1950,2015])

axes[0].legend(ncol=4,frameon=False)
axes[1].legend(ncol=4,frameon=False)
axes[2].legend(ncol=4,frameon=False)
plt.tight_layout()
plt.savefig('Figures/ohc_obs.png')
plt.show()
