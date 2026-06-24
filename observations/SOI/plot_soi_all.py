import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (15,4)


def read_soi_monthly(filename):
    c=pd.read_csv(filename, sep=",",header=0,index_col=0)
    print(c)
    df_soi = pd.DataFrame(data=[],columns=['SOIindex'])
    for year in c.index:
        yearlist = np.arange(year,year+1,1/12)
        df_soi_mon = pd.DataFrame(data=c.loc[year].values,index=yearlist,columns=['SOIindex'])
        print(df_soi_mon)
        df_soi = pd.concat([df_soi,df_soi_mon])

    return df_soi


filepath = '/div/qbo/utrics/Observations/Observations_06_2023/ElNino/'
filename = filepath + 'soi_index.csv'
df_obs = read_soi_monthly(filename)

#Plot timeseries
print(df_obs)
df_obs.plot(color='k',zorder=10,label='SOIIndex')



model_list = [ 'CNRM-CM6-1', 'HadGEM3-GC31-LL', 'NorESM2-MM',  'NorESM2-LM']
ens_list_models = {'CNRM-CM6-1': ['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10',
                                  'r11','r12','r13','r14','r15','r16','r17','r18','r19','r20',
                                  'r21','r22','r23','r24','r25','r26','r27','r28','r29','r30'],
                   'HadGEM3-GC31-LL': ['r1','r2','r3','r4'],
                   'NorESM2-MM':['r1','r2','r3'],
                   'NorESM2-LM':['r1','r2','r3']}

ncol_models = { 'CNRM-CM6-1':15+1,
                'HadGEM3-GC31-LL':4+1,
                'NorESM2-MM':3+1,
                'NorESM2-LM':3+1}


fig, axs = plt.subplots(4,1,figsize=(20,15))

for m,model in enumerate(model_list):
    ens_list = ens_list_models[model]

    
    for ens in ens_list:
        filename = model + '_' + ens + '_cmip6_soi.csv'
                     
        df_mod = read_soi_monthly(filename)
        
        axs[m].plot(df_mod, linewidth = 0.5,label = ens)

    axs[m].set_title(model)
    
    axs[m].axhline(y=-7,color='gray')
    axs[m].axhline(y=7,color='gray')
    
    
    axs[m].set_xlim([1850,2024])
    axs[m].set_ylabel('SOI index')
        
    axs[m].plot(df_obs,color='k',linewidth=0.5,label='SOI-index')
    axs[m].legend(ncol=ncol_models[model],frameon=False)



plt.savefig('../../Figures/soi.png')
  
plt.show()
