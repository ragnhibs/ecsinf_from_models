import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm



plt.rcParams['font.size'] = 5
plt.rcParams['figure.dpi'] = 300

fullname = {'CNRM1':'CNRM-CM6-1',
            'NorESM2MM':'NorESM2MM',
            'NorESM2LM': 'NorESM2LM',
            'HadGEM3':'HadGEM3 GC3.1-LL'}

model_list = ['CNRM1',
              'HadGEM3',
              'NorESM2MM',
              'NorESM2LM']

ens_list = {'CNRM1':np.arange(1,31,1),
            'HadGEM3':np.arange(1,5,1),
            'NorESM2MM': np.arange(1,4,1),
            'NorESM2LM': np.arange(1,4,1)} 




color_list = {'CNRM1':'tab:blue',
              'HadGEM3':'tab:green',      
              'NorESM2MM':'tab:purple',
              'NorESM2LM':'tab:orange'}

#Number of ensambles in total:
antscen = 0
for model in model_list:
    antscen = antscen+ens_list[model][-1]
print(antscen)
antscen = antscen + 1 #To make a space in figure


fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(6,5))
axs.axhspan(0, -5, facecolor='lightgray', alpha=0.3, zorder=0)


sc = 0
label_mean = 'Mean'
label_95 = '90% C.I.'
for model in model_list:
    for ens in ens_list[model]:

        sc = sc + 1
        scen = 'OutputAnalyse'+model+ 'R' + str(ens)
        summary_tcr = pd.read_csv('results_csv/summary_tcr_'
                                  + scen + '.csv',
                                  index_col=0)
        print(summary_tcr)
        
        axs.plot(summary_tcr['Mean'],antscen-sc,'o',markersize=3,
                 color=color_list[model],label=label_mean)
        #axs.plot(summary_tcr['Median'],0.2+0.05*sc,'d',color=colorlist[sc])
        axs.plot([summary_tcr['5perc'],summary_tcr['95perc']],
                 [antscen-sc, antscen-sc],'-',linewidth=1,color=color_list[model],
                 label=label_95)
        if sc == 1:
            summary_all = summary_tcr
        else:
            summary_all = pd.concat([summary_all,summary_tcr])
        
        label_mean = None
        label_95 = None
        
        textline = fullname[model] + ' r'+ str(ens)
        axs.text(4,antscen-sc+0.1,textline,color=color_list[model])


pd.options.display.float_format = '{:,.2f}'.format
#summary_all = summary_all.rename(index=scen_list_out)
print(summary_all)

#From Table 7.SM.5 in IPCC AR6
cnrm_tcr = 2.14
hadgem_tcr = 2.55
noresmLM_tcr = 1.48
noresmMM_tcr = 1.33





axs.plot(cnrm_tcr,-1,'s',color=color_list['CNRM1'],linewidth=1,markersize=3,label=fullname['CNRM1'])
axs.axvline(cnrm_tcr,linestyle='--',color=color_list['CNRM1'],linewidth=0.1)
axs.text(4,-1.0,fullname['CNRM1'],color=color_list['CNRM1'])

axs.plot(hadgem_tcr,-2,'s',color=color_list['HadGEM3'],linewidth=1,markersize=3,label=fullname['HadGEM3'])
axs.axvline(hadgem_tcr,linestyle='--',color=color_list['HadGEM3'],linewidth=0.1)
axs.text(4,-2.0,fullname['HadGEM3'],color=color_list['HadGEM3'])


axs.plot(noresmLM_tcr,-3,'s',color=color_list['NorESM2LM'],linewidth=1,markersize=3,label=fullname['NorESM2LM'])
axs.axvline(noresmLM_tcr,linestyle='--',color=color_list['NorESM2LM'],linewidth=0.1)
axs.text(4,-3.0,fullname['NorESM2LM'],color=color_list['NorESM2LM'])

axs.plot(noresmMM_tcr,-4,'s',color=color_list['NorESM2MM'],linewidth=1,markersize=3,label=fullname['NorESM2MM'])
axs.axvline(noresmMM_tcr,linestyle='--',color=color_list['NorESM2MM'],linewidth=0.1)
axs.text(4,-4.0,fullname['NorESM2MM'],color=color_list['NorESM2MM'])


ipcc_central = 1.8
ipcc_likely = [1.4,2.2]
ipcc_very_likely = [1.2,2.4]

axs.plot(ipcc_central, -6,'s',color='darkgray',linewidth=1,markersize=3,label='TCR IPCC central')
axs.plot(ipcc_likely,[-6,-6], color='darkgray',linewidth=1,label='TCR IPCC likely')
axs.plot(ipcc_very_likely,[-6,-6], linestyle='--',linewidth=1,
         color='darkgray',label='TCR IPCC very likely')

axs.text(4,-6.0,'IPCC AR6',color='darkgray')

axs.set_yticks([])
axs.set_xlim(-0.5,5.5)
axs.set_xticks([0,0.5,1,1.5,2,2.5,3,3.5,4])
axs.set_ylim(-7,antscen+1)

axs.set_xlabel('Transient Climate Response (TCR) [K]') 
plt.legend(loc='upper left',frameon=False)
plt.savefig('Figures/TCR.png')







#Text to manusctipt:
print('Text to manuscript')


cnrm_rows = summary_all[summary_all.index.str.contains('CNRM')]

print('Ensemble larger mean than TCR')
print(cnrm_rows[cnrm_rows['Mean'] > cnrm_tcr]) 



summary_all.to_csv('Figures/tcr.csv')











plt.show()
