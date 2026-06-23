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


fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(5,5))
axs.axhspan(antscen+1, antscen+6, facecolor='lightgray', alpha=0.3, zorder=0)
sc = 0
label_mean = 'Mean'
label_95 = '90% C.I.'

for model in model_list:
    for ens in ens_list[model]:

        sc = sc + 1
        scen = 'OutputAnalyse'+model+ 'R' + str(ens)
        summary_ecs_inf = pd.read_csv('results_csv/summary_ecs_inf_'
                                  + scen + '.csv',
                                  index_col=0)
        

        summary_ecs_inf.index = [fullname[model] + ' r'+ str(ens)]
        
        axs.plot(summary_ecs_inf['Mean'],antscen-sc,'o',markersize=3,
                 color=color_list[model],label=label_mean)

        #axs.plot(summary_ecs_inf['Median'],antscen-sc,'d',color=color_list[model])

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
        axs.text(-1.5,antscen-sc-0.25,textline,color=color_list[model])


pd.options.display.float_format = '{:,.2f}'.format
#summary_all = summary_all.rename(index=scen_list_out)
print(summary_all)
summary_all.to_csv('Figures/ECSinf.csv')

#Values from ipcc AR6 table X:
#Table 7.SM.5 | Equilibrium climate sensitivity (ECS)
cnrm_ecs_ar6 = 4.83
hadgem_ecs_ar6 = 5.55
noresmLM_ecs_ar6 = 2.54
noresmMM_ecs_ar6 = 2.50


#Values from Zelinka:
cnrm_ecs = 4.9
hadgem_ecs = 5.55
noresmLM_ecs = 2.56



axs.plot(cnrm_ecs_ar6,antscen+5,'s',color=color_list['CNRM1'],linewidth=1,markersize=3,label='CNRM-CM6-1')
#axs.plot(cnrm_ecs,-1,'d',color=color_list['CNRM1'],linewidth=1,markersize=3)

axs.axvline(cnrm_ecs_ar6,linestyle='--',color=color_list['CNRM1'],linewidth=0.1)
axs.text(-1.5,antscen+5-0.25,'ECS: CNRM-CM6-1',color=color_list['CNRM1'])


axs.plot(hadgem_ecs_ar6,antscen+4,'s',color=color_list['HadGEM3'],linewidth=1,markersize=3,label='HadGEM3-GC31-LL')
#axs.plot(hadgem_ecs,-2,'d',color=color_list['HadGEM3'],linewidth=1,markersize=3)
axs.axvline(hadgem_ecs_ar6,linestyle='--',color=color_list['HadGEM3'],linewidth=0.1)
axs.text(-1.5,antscen+4-0.25,'ECS: HadGEM3-GC31-LL',color=color_list['HadGEM3'])


axs.plot(noresmLM_ecs_ar6,antscen+2,'s',color=color_list['NorESM2LM'],linewidth=1,markersize=3,label='NorESM2-LM')
#axs.plot(noresmLM_ecs,-3,'d',color=color_list['NorESM2LM'],linewidth=1,markersize=3)
axs.axvline(noresmLM_ecs_ar6,linestyle='--',color=color_list['NorESM2LM'],linewidth=0.1)
axs.text(-1.5,antscen+2-0.25,'ECS: NorESM2-LM',color=color_list['NorESM2LM'])


axs.plot(noresmMM_ecs_ar6,antscen+3,'s',color=color_list['NorESM2MM'],linewidth=1,markersize=3,label='NorESM2-MM')

axs.axvline(noresmMM_ecs_ar6,linestyle='--',color=color_list['NorESM2MM'],linewidth=0.1)
axs.text(-1.5,antscen+3-0.25,'ECS: NorESM2-MM',color=color_list['NorESM2MM'])



axs.set_yticks([])
axs.set_xlim(-2,11)
axs.set_ylim(0,antscen+7)

axs.set_xlabel('Inferred Effective Climate Sensitivity (ECS$_{inf}$) [K]') 

axs.set_xticks([0,2,4,6,8,10])

plt.legend(loc='lower right',frameon=False)
plt.savefig('Figures/ECSinf.png')






#Text to manusctipt:
print('Text to manuscript')


cnrm_rows = summary_all[summary_all.index.str.contains('CNRM')]
print('CNRM max min')
print("{:.2f}".format(cnrm_rows['Mean'].max()))
print("{:.2f}".format(cnrm_rows['Mean'].min()))

print('Ensemble larger mean than ECS')
print(cnrm_rows[cnrm_rows['Mean'] > cnrm_ecs_ar6]) 


print('Upper close to ECS')
print(cnrm_rows[cnrm_rows['95perc'] - cnrm_ecs_ar6 < 0.2]) 
print(cnrm_rows[abs(cnrm_rows['95perc'] - cnrm_ecs_ar6) < 0.2])

print('Mean ECSinf ~ ECS')
print(cnrm_rows[abs(cnrm_rows['Mean'] - cnrm_ecs_ar6) < 0.3]) 

print('HadGEM')
hadgem_rows = summary_all[summary_all.index.str.contains('HadGEM')]
print(hadgem_rows['Mean']-hadgem_ecs_ar6)
print('diff max min HadGEM')
print(hadgem_rows['Mean'].max()- hadgem_rows['Mean'].min())


print('diff max min CNRM')
print(cnrm_rows['Mean'].max()- cnrm_rows['Mean'].min())




plt.show()
