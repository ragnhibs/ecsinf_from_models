import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


plt.rcParams['font.size'] = 5
plt.rcParams['figure.dpi'] = 300

fullname = {'CNRM1':'CNRM-CM6-1',
            'HadGEM3':'HadGEM3-GC31-LL',
            'NorESM2LM':'NorESM2-LM',
            'NorESM2MM':'NorESM2-MM'}


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


fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(6,4))

sc = 0
label_mean = 'Mean'
label_95 = '90% C.I.'

for model in model_list:
    for ens in ens_list[model]:

        sc = sc + 1
        scen = 'OutputAnalyse'+model+ 'R' + str(ens)
        summary_ecs_inf = pd.read_csv('results_csv/summary_pattern_'
                                  + scen + '.csv',
                                  index_col=0)
        print(summary_ecs_inf)
        
        axs.plot(summary_ecs_inf['Mean'],antscen-sc,'o',markersize=3,
                 color=color_list[model],label=label_mean)
        #axs.plot(summary_ecs_inf['Median'],0.2+0.05*sc,'d',color=colorlist[sc])
        axs.plot([summary_ecs_inf['5perc'],summary_ecs_inf['95perc']],
                 [antscen-sc, antscen-sc],'-',linewidth=1,color=color_list[model],
                 label=label_95)
        if sc == 1:
            summary_all = summary_ecs_inf
        else:
            summary_all = pd.concat([summary_all,summary_ecs_inf])
        
        label_mean = None
        label_95 = None
        
        textline = fullname[model] + ' r'+ str(ens)
        axs.text(-1.5,antscen-sc+0.1,textline,color=color_list[model])


pd.options.display.float_format = '{:,.2f}'.format
#summary_all = summary_all.rename(index=scen_list_out)
print(summary_all)



axs.axvspan(0,1, alpha=0.5, color='lightgray',zorder=-10)

axs.set_yticks([])
axs.set_xlim(-1.6,3)
axs.set_xticks([0,0.5,1,1.5,2,2.5,3])
#axs.set_ylim(-6,antscen+1)

axs.set_xlabel(' $\\alpha^\'$ \"Pattern effect\"  [W m$^{-2}$  K^${-1}$]') 

plt.legend(loc='upper right',frameon=False)
plt.savefig('Figures/pattern.png')
plt.show()
