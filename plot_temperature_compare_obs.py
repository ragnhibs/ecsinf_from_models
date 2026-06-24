import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams['font.size'] = 4
plt.rcParams['figure.dpi'] = 300

obslist_out = {'noaa':'NOAA',
               'giss':'GISS',
               'hadcrut':'HADCRUT'}

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


filepath_obs = 'observations/TEMP/'


fig, axs = plt.subplots(3,1, sharex=True,sharey=True,figsize=(14/3.5,18/3.5))

for model in model_list:

    
    for ens in ens_list[model]:
        sc = ens-1  # For colorlist
        
        #scen = 'OutputAnalyse'+model+ 'R' + str(ens)

        
        #Plot "observations"
        
        ens_org = 'r'+str(ens)+ens_name[model]
        file_nh = 'temp_nh_'+model_org[model] +'_'+ens_org+'.csv'
        file_sh = 'temp_sh_'+model_org[model] +'_'+ens_org+'.csv'

        data_sh = pd.read_csv(filepath_obs + file_sh,index_col=0)
        data_nh = pd.read_csv(filepath_obs + file_nh,index_col=0)
        
        if ens == 1:
            axs[0].plot(data_nh['anomaly'],linewidth=0.5,linestyle='-',label=model_org[model],color=color_list[model])
            axs[1].plot(data_sh['anomaly'],linewidth=0.5,linestyle='-',label=model_org[model],color=color_list[model])
            axs[2].plot((data_nh['anomaly']+data_sh['anomaly'])*0.5,linewidth=0.5,
                        linestyle='-',label=model_org[model],color=color_list[model])

        else:
            axs[0].plot(data_nh['anomaly'],linewidth=0.5,linestyle='-',color=color_list[model])
            axs[1].plot(data_sh['anomaly'],linewidth=0.5,linestyle='-',color=color_list[model])
            axs[2].plot((data_nh['anomaly']+data_sh['anomaly'])*0.5,linewidth=0.5,
                        linestyle='-',color=color_list[model])
            

axs[0].text(0.02, 1.1, '(a)', transform=axs[0].transAxes, fontsize=7, va='top', ha='right')
axs[1].text(0.02, 1.1, '(b)', transform=axs[1].transAxes, fontsize=7, va='top', ha='right')
axs[2].text(0.02, 1.1, '(c)', transform=axs[2].transAxes, fontsize=7, va='top', ha='right')
        
axs[1].legend(loc='upper left')
axs[0].legend(loc='upper left')
axs[2].legend(loc='upper left')

axs[0].set_xlim(1850,2020)
axs[1].set_xlim(1850,2020)
axs[2].set_xlim(1850,2020)


axs[0].set_ylabel('NHMST [$^\circ$C] (anomalies relative to 1960 to 1990)')
axs[1].set_ylabel('SHMST [$^\circ$C] (anomalies relative to 1960 to 1990) ')
axs[2].set_ylabel('GMST [$^\circ$C] (anomalies relative to 1960 to 1990)')

plt.tight_layout()
plt.savefig('Figures/temp_obs.png')



plt.show()
