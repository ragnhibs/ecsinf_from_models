import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import string


plt.rcParams['font.size'] = 5
plt.rcParams['figure.dpi'] = 300

def plot_obs_temp():
    for en in ens_list[model]:
        ens_org = 'r'+str(en)+ens_name[model]
        file_nh = 'temp_nh_'+model_org[model] +'_'+ens_org+'.csv'
        file_sh = 'temp_sh_'+model_org[model] +'_'+ens_org+'.csv'
        
        data_sh = pd.read_csv(filepath_obs + file_sh,index_col=0)
        data_nh = pd.read_csv(filepath_obs + file_nh,index_col=0)
        if en == ens:
            axs[1,m].plot((data_nh['anomaly']+data_sh['anomaly'])*0.5,linewidth=1,
                        linestyle='-',color='black',label='"obs."') 
        elif en==2: 
            axs[1,m].plot((data_nh['anomaly']+data_sh['anomaly'])*0.5,linewidth=0.5,zorder=-10,
                          linestyle='-',color='gray',label='other "obs."')
        else: 
            axs[1,m].plot((data_nh['anomaly']+data_sh['anomaly'])*0.5,linewidth=0.5,zorder=-10,
                          linestyle='-',color='gray')
    
def plot_temp():
    ens_org = 'r'+str(ens)+ens_name[model]
    scen = 'OutputAnalyse'+model+ 'R' + str(ens)

    post_temp_NH= pd.read_csv('results_csv/post_'+scen+'_temp_NH.txt',index_col=0)
    post_temp_SH= pd.read_csv('results_csv/post_'+scen+'_temp_SH.txt',index_col=0)
    post_temp_glob = 0.5*(post_temp_NH + post_temp_SH)
    
    yearlist = post_temp_glob.columns.values.astype(float)
    
    #Global
    axs[1,m].fill_between(yearlist, np.percentile(post_temp_glob.values,5, axis=0),
                        np.percentile(post_temp_glob.values, 95, axis=0), linewidth=0.25,color='red', alpha=0.3,label='90 C.I.')
    axs[1,m].plot(yearlist,np.percentile(post_temp_glob.values,50, axis=0),color='red',label='Posterior mean')
    

def plot_ohc_obs():
    for en in ens_list[model]:
        file_cmip = 'ohc_700_bot_'+model_org[model]+ '_r'+str(en)+'.csv'
        cmip_700_bot = pd.read_csv('./observations/OHC/'+file_cmip,index_col=0)
        file_cmip = 'ohc_0_700_'+model_org[model]+ '_r'+str(en)+'.csv'
        cmip_0_700 = pd.read_csv('./observations/OHC/'+file_cmip,index_col=0)

        if en == ens:
            axs[2,m].plot(cmip_0_700+cmip_700_bot,linewidth = 1,linestyle='-',color='black', label='"obs."')
        elif en == 2:
            axs[2,m].plot(cmip_0_700+cmip_700_bot,linewidth = 0.5,linestyle='-',zorder=-10,color='gray',label='other "obs."')
        else:
            axs[2,m].plot(cmip_0_700+cmip_700_bot,linewidth = 0.5,linestyle='-',zorder=-10,color='gray')

def plot_ohc():
    scen = 'OutputAnalyse'+model+ 'R' + str(ens)
    post_OHCto700= pd.read_csv('results_csv/post_'+scen+'_OHCto700.txt',index_col=0)
    post_OHCbelow700= pd.read_csv('results_csv/post_'+scen+'_OHCbelow700.txt',index_col=0)
    post_OHCtot = post_OHCto700 + post_OHCbelow700
    
    post_OHCtot.replace(20000, np.nan, inplace=True)
    yearlist = post_OHCtot.columns.values.astype(int)
    
    axs[2,m].fill_between(yearlist, np.percentile(post_OHCtot.values,5, axis=0),
                        np.percentile(post_OHCtot.values, 95, axis=0), linewidth=0.25,color='red', alpha=0.3,label='90 C.I.')
    
    axs[2,m].plot(yearlist,np.percentile(post_OHCtot.values,50, axis=0),color='red',label='Posterior mean')
    


def plot_post_erf():
    scen = 'OutputAnalyse'+model+ 'R' + str(ens)
    rf_comp ='Tot'
    filename = 'summary_rf_post_timeseries_all_perc_'+rf_comp+scen+'.csv'

    
    post_rf=pd.read_csv('results_csv/'+filename,
                        index_col=0)
    
    axs[0,m].plot(post_rf['Median'],color='black',linewidth=1,label='Posterior mean')
    axs[0,m].fill_between(post_rf.index, post_rf['5perc'],
                          post_rf['95perc'],
                          linewidth=0.25,
                          color='black',
                          alpha=0.3,label='90 C.I.')



def plot_tastrend():
    figfile = './TAS_plot/Fig/tastrend_19802014_'+model_org[model]+'_r'+str(ens)+'.png'
    img = mpimg.imread(figfile)

  
    
    axs[3,m].imshow(img)
    axs[3,m].axis('off')



def add_title():
    #Values from ipcc AR6 table X:
    #Table 7.SM.5 | Equilibrium climate sensitivity (ECS)
    cnrm_ecs_ar6 = 4.83
    hadgem_ecs_ar6 = 5.55
    noresmLM_ecs_ar6 = 2.54
    noresmMM_ecs_ar6 = 2.50

    ecs_list = {'CNRM1':cnrm_ecs_ar6,
                'HadGEM3':hadgem_ecs_ar6,
                'NorESM2LM':noresmLM_ecs_ar6,
                'NorESM2MM': noresmMM_ecs_ar6}

    summary_all = pd.read_csv('Figures/ECSinf.csv',index_col=0)

    
    ecs_mean = summary_all['Mean'].loc[model_org[model] + ' r'+str(ens)]
    ecs_mod = ecs_list[model]
    delta = ecs_mean - ecs_mod
    print(delta)
    print(ecs_mean)
    print(delta/ecs_mod*100)

    
    return '{:.1f}'.format(ecs_mean) + '$^\circ$C [' + '{:.2f}'.format(delta)+ '$^\circ$C, '+ '{:.1f}'.format(delta/ecs_mod*100.0) + '%]'

    

    #return textstring
    
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

color_list = {'CNRM1':'lightblue',
              'HadGEM3':'darkgreen',
              'NorESM2MM':'darkred',
              'NorESM2LM':'orange'}

filepath_obs = './observations/TEMP/'

#Plot total posteriori RF, Prior and post GMST, Prior and post OHC tot

# Create an array of lowercase letters
letters = list(string.ascii_lowercase)


fig, axs = plt.subplots(4,4,figsize=(22/2.5,17/2.5))
for m,model in enumerate(model_org):
    print(model)
    for ens in np.arange(1,2,1): #ens_list[model]:
        
        print(ens)
        plot_post_erf()
        plot_temp()
        plot_obs_temp()
        plot_ohc()
        plot_ohc_obs()
        plot_tastrend()

        ecs_summary = add_title()

        
        axs[0,m].set_title(model_org[model] + ' r'+ str(ens) + ens_name[model] + ' \n' +ecs_summary)
        axs[0,m].set_ylabel('Total ERF [W m$^{-2}$]')
        axs[0,m].legend(loc='upper left')
        axs[0,m].axhline(y=0.0,color='darkgray',linestyle='--')
        
        axs[0,m].set_xlim(1850,2020)
        axs[0,m].set_ylim(-1,2.1)
        
        
        axs[1,m].legend(loc='upper left')
        axs[1,m].set_ylabel('GMST (relative to 1960-1990) [$^\circ$C]')
        axs[1,m].set_xlim(1850,2020)
        axs[1,m].set_ylim(-1,1.6)
        
        
       
        axs[2,m].set_ylabel('Total OHC (relative to 1990-2014) [10$^{22}$ Joule]')
        axs[2,m].set_ylim([-30,12])
        axs[2,m].set_xlim([1850,2020])
        axs[2,m].legend(loc='upper left')

        #plt.suptitle(model +  ' r'+str(ens)+ens_name[model])




for a,ax in enumerate(axs.flatten()):
    ax.set_title('('+letters[a]+')',loc='left')

plt.tight_layout()
plt.savefig('Figures_ens/combined_results_all_models_'+str(ens)+'.png')

plt.close(fig)
