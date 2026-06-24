import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def plot_intvar():
     scen = 'OutputAnalyse'+model+ 'R' + str(ens)

     post_intvar_NH= pd.read_csv('results_csv/summary_posterior_intvar_temp_nh_'+scen+'.csv',index_col=0)
     post_intvar_SH= pd.read_csv('results_csv/summary_posterior_intvar_temp_sh_'+scen+'.csv',index_col=0)
     post_intvar_glob= pd.read_csv('results_csv/summary_posterior_intvar_temp_glob_'+scen+'.csv',index_col=0)

     plott = post_intvar_NH
     axs[row,0].fill_between(plott.index,plott['95perc'],
                           plott['5perc'],
                           color='green', alpha=0.3)
     axs[row,0].plot(plott['Median'],
                   color='green',label=scen)
     if row==0: axs[0,0].set_title('Long term internal variability')

     plott = post_intvar_SH
     axs[row,0].fill_between(plott.index,plott['95perc'],
                           plott['5perc'],
                           color='orange', alpha=0.3)
     axs[row,0].plot(plott['Median'],
                   color='orange',label=scen)
     axs[row,0].axhline(0.0,linestyle='--',color='gray')    

     axs[row,0].set_ylim([-0.5,0.5])
     axs[row,0].set_ylabel('Temperature $^\circ$C',fontsize=7)
     axs[row,0].text(0.05, 0.95, ens, transform=axs[row,0].transAxes, fontsize=14, fontweight=fontweight,verticalalignment='top')
     
def plot_enso():
    scen = 'OutputAnalyse'+model+ 'R' + str(ens)

    post_enso_NH= pd.read_csv('results_csv/summary_posterior_elnino_nh_'+scen+'.csv',index_col=0)
    post_enso_SH= pd.read_csv('results_csv/summary_posterior_elnino_sh_'+scen+'.csv',index_col=0)
    post_enso_glob= pd.read_csv('results_csv/summary_posterior_elnino_glob_'+scen+'.csv',index_col=0)
    plott = post_enso_NH
    axs[row,1].fill_between(plott.index,plott['95perc'],
                            plott['5perc'],
                            color='green', alpha=0.3)
    axs[row,1].plot(plott['Median'],
                    color='green',label=scen)
    if row==0: axs[0,1].set_title('ENSO variability')
    
    plott = post_enso_SH
    axs[row,1].fill_between(plott.index,plott['95perc'],
                            plott['5perc'],
                            color='orange', alpha=0.3)
    axs[row,1].plot(plott['Median'],
                    color='orange',label=scen)
    axs[row,1].axhline(0.0,linestyle='--',color='gray')    
    
    axs[row,1].set_ylim([-0.5,0.5])
    axs[row,1].set_ylabel('Temperature $^\circ$C',fontsize=7)
    axs[row,1].text(0.05, 0.95, ens, transform=axs[row,1].transAxes, fontsize=14, fontweight=fontweight,verticalalignment='top')

def plot_noise():
    scen = 'OutputAnalyse'+model+ 'R' + str(ens)

    post_noise_NH= pd.read_csv('results_csv/summary_posterior_noise_temp_nh_'+scen+'.csv',index_col=0)
    post_noise_SH= pd.read_csv('results_csv/summary_posterior_noise_temp_sh_'+scen+'.csv',index_col=0)
    post_noise_glob= pd.read_csv('results_csv/summary_posterior_noise_temp_glob_'+scen+'.csv',index_col=0)
        
    
    plott = post_noise_NH
    axs[row,2].fill_between(plott.index,plott['95perc'],
                            plott['5perc'],
                            color='green', alpha=0.3)
    axs[row,2].plot(plott['Median'],
                    color='green',label=scen)
    if row==0: axs[0,2].set_title('Noise')
    
    plott = post_noise_SH
    axs[row,2].fill_between(plott.index,plott['95perc'],
                            plott['5perc'],
                            color='orange', alpha=0.3)
    axs[row,2].plot(plott['Median'],
                    color='orange',label=scen)
    axs[row,2].axhline(0.0,linestyle='--',color='gray')    
    
    axs[row,2].set_ylim([-0.5,0.5])
    axs[row,2].set_ylabel('Temperature $^\circ$C',fontsize=7)
    axs[row,2].text(0.05, 0.95, ens, transform=axs[row,2].transAxes, fontsize=14, fontweight=fontweight,verticalalignment='top')

def plot_ohc_intvar():
    scen = 'OutputAnalyse'+model+ 'R' + str(ens)

    post_intvar_ohc_above700= pd.read_csv('results_csv/summary_posterior_intvar_ohc_above700_'+scen+'.csv',index_col=0)
    post_intvar_ohc_below700= pd.read_csv('results_csv/summary_posterior_intvar_ohc_below700_'+scen+'.csv',index_col=0)
    
    plott = post_intvar_ohc_above700
    axs[row,4].fill_between(plott.index,plott['95perc'],
                          plott['5perc'],
                          color='red', alpha=0.3)
    axs[row,4].plot(plott['Median'],
                color='red',label=scen)

    if row==0: axs[row,4].set_title('Long term internal variability')

    plott = post_intvar_ohc_below700
    axs[row,4].fill_between(plott.index,plott['95perc'],
                          plott['5perc'],
                          color='blue', alpha=0.3)
    axs[row,4].plot(plott['Median'],
                color='blue',label=scen)

    axs[row,4].axhline(0.0,linestyle='--',color='gray')
    axs[row,4].set_ylim([-6,6])
    axs[row,4].set_ylabel('Ocean Heat Content $10^{22}$J',fontsize=7)
    axs[row,4].text(0.05, 0.95, ens, transform=axs[row,4].transAxes, fontsize=14, fontweight=fontweight,verticalalignment='top')

def plot_ohc_noice():
    scen = 'OutputAnalyse'+model+ 'R' + str(ens)
    post_noise_ohc_above700= pd.read_csv('results_csv/summary_posterior_noise_ohc_above700_'+scen+'.csv',index_col=0)
    post_noise_ohc_below700= pd.read_csv('results_csv/summary_posterior_noise_ohc_below700_'+scen+'.csv',index_col=0)
    plott = post_noise_ohc_above700
    axs[row,3].fill_between(plott.index,plott['95perc'],
                          plott['5perc'],
                          color='red', alpha=0.3)
    axs[row,3].plot(plott['Median'],
                  color='red',label=scen)
    if row==0: axs[row,3].set_title('Model error ohc')
    plott = post_noise_ohc_below700
    axs[row,3].fill_between(plott.index,plott['95perc'],
                          plott['5perc'],
                          color='blue', alpha=0.3)
    axs[row,3].plot(plott['Median'],
                  color='blue',label=scen)
   
    
    axs[row,3].axhline(0.0,linestyle='--',color='gray')
    axs[row,3].set_ylim([-6,6])
    axs[row,3].set_ylabel('Ocean Heat Content $10^{22}$J',fontsize=7)
    axs[row,3].text(0.05, 0.95, ens, transform=axs[row,3].transAxes, fontsize=14, fontweight=fontweight, verticalalignment='top')




### Add "observations":
model_org = {'CNRM1':'CNRM-CM6-1',
             'HadGEM3':'HadGEM3-GC31-LL',
             'NorESM2LM':'NorESM2-LM',
             'NorESM2MM':'NorESM2-MM'}

ens_name = {'CNRM1':'i1p1f2',
            'HadGEM3': 'i1p1f3',
            'NorESM2LM':'i1p1f1',
            'NorESM2MM':'i1p1f1'}

color_list = {'CNRM1':'lightblue',
              'HadGEM3':'darkgreen',
              'NorESM2MM':'darkred',
              'NorESM2LM':'orange'}



fig, axs = plt.subplots(8,5,figsize=(28,15))

fontweight = 'heavy'

ens_list = [2,11,21,22,25,29]

model = 'CNRM1'
for ens in np.arange(1,9):
     if ens in ens_list:
          fontweight = 'heavy'
     else:
          fontweight = 'normal'
          
     
     
     print(ens)
     row = ens-1
     plot_intvar()
     plot_enso()
     plot_noise()
     plot_ohc_intvar()
     plot_ohc_noice()
plt.suptitle(model_org[model])
plt.tight_layout()
plt.savefig('Figures/errorterms_CNRM1_1.png')

fig, axs = plt.subplots(8,5,figsize=(28,15))

model = 'CNRM1'
for ens in np.arange(9,17):
     if ens in ens_list:
          fontweight = 'heavy'
     else:
          fontweight = 'normal'

     print(ens)
     row = ens-9
     plot_intvar()
     plot_enso()
     plot_noise()
     plot_ohc_intvar()
     plot_ohc_noice()


    
plt.suptitle(model_org[model])
plt.tight_layout()
plt.savefig('Figures/errorterms_CNRM1_2.png')

fig, axs = plt.subplots(8,5,figsize=(28,15))

model = 'CNRM1'
for ens in np.arange(17,25):
     if ens in ens_list:
          fontweight = 'heavy'
     else:
          fontweight = 'normal'

     print(ens)
     row = ens-17
     plot_intvar()
     plot_enso()
     plot_noise()
     plot_ohc_intvar()
     plot_ohc_noice()
     

    
plt.suptitle(model_org[model])    
plt.tight_layout()
plt.savefig('Figures/errorterms_CNRM1_3.png')

fig, axs = plt.subplots(8,5,figsize=(28,15))

model = 'CNRM1'
for ens in np.arange(25,31):
     if ens in ens_list:
          fontweight = 'heavy'
     else:
          fontweight = 'normal'
     print(ens)
          
     row = ens-25
     plot_intvar()
     plot_enso()
     plot_noise()
     plot_ohc_intvar()
     plot_ohc_noice()
plt.suptitle(model_org[model])
plt.tight_layout()
plt.savefig('Figures/errorterms_CNRM1_4.png')

fig, axs = plt.subplots(4,5,figsize=(28,10))

ens_list = [1,2]
model = 'HadGEM3'
for ens in np.arange(1,5):
     if ens in ens_list:
          fontweight = 'heavy'
     else:
          fontweight = 'normal'
     print(ens)

     print(ens)
     row = ens-1
     plot_intvar()
     plot_enso()
     plot_noise()
     plot_ohc_intvar()
     plot_ohc_noice()
plt.suptitle(model_org[model])    
plt.tight_layout()
plt.savefig('Figures/errorterms_HadGEM3.png')

fig, axs = plt.subplots(3,5,figsize=(28,10)) 
model = 'NorESM2MM'
for ens in np.arange(1,4):
     if ens == 1:
          fontweight = 'heavy'
     else:
          fontweight = 'normal' 
     print(ens)
     row = ens-1
     plot_intvar()
     plot_enso()
     plot_noise()
     plot_ohc_intvar()
     plot_ohc_noice()
plt.suptitle(model_org[model])
plt.tight_layout()
plt.savefig('Figures/errorterms_NorESM2MM.png')

fig, axs = plt.subplots(3,5,figsize=(28,10)) 
model = 'NorESM2LM'
for ens in np.arange(1,4):
     fontweight = 'normal' 
     print(ens)
     row = ens-1
     plot_intvar()
     plot_enso()
     plot_noise()
     plot_ohc_intvar()
     plot_ohc_noice()

    
plt.suptitle(model_org[model])    
plt.tight_layout()
plt.savefig('Figures/errorterms_NorESM2LM.png')
plt.show()

