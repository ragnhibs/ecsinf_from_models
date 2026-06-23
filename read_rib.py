import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


filepath = '/div/qbo/utrics/ClimateSensitivity/UseCMIP6/RESULTS/'

"""
ens_list = {'CNRM1':np.arange(1,31,1),
            'HadGEM3':np.arange(1,5,1),
            'NorESM2MM': np.arange(1,4,1),
            'NorESM2LM': np.arange(1,4,1)} 

filepath_cataloge = {'CNRM1':'CNRM_R1-R30',
                     'HadGEM3':'HadGEM_R1-R4',
                     'NorESM2MM':'NorESM2',
                     'NorESM2LM':'NorESM2'}

#model_list = ['CNRM1',
#              'HadGEM3',
#              'NorESM2MM',
#              'NorESM2LM']


#model_list = ['NorESM2MM',
#              'NorESM2LM']
"""


model_list = ['CNRM1']
ens_list = {'CNRM1':[23]}
filepath_cataloge = {'CNRM1':'CNRM1R23'}


filename = 'postRIB.txt'

for model in model_list:
    for ens in ens_list[model]:
        scen = 'OutputAnalyse'+model+'R'+str(ens)
        

        post_rib= pd.read_csv(filepath+filepath_cataloge[model]+'/'+scen+'/'+filename,sep=' ',header=None)
    
    
        year_start = 1850
        year_end = 2014
        antyr = year_end-year_start
    
    
        yearlist = np.arange(year_start,year_end+1,1)
    
        post_rib = post_rib.loc[:,0:antyr]
        post_rib.columns = yearlist
    
        samples = len(post_rib.index)
        bin = (int(samples*0.001))
    
        print(post_rib)
    
        fig, axs = plt.subplots(nrows=1,ncols=2,figsize=(11,6))
        axs[0].fill_between(yearlist, np.percentile(post_rib,5, axis=0),
                            np.percentile(post_rib, 95, axis=0), color='k',
                            alpha=0.3,label='90CI')
    
        axs[0].set_ylabel('W m$^{-2}$')
        axs[0].axhline(0.0,linestyle='--',color='gray')
    
        #Write to file:
        d = {'Median': np.percentile(post_rib,50, axis=0),
             '5perc':np.percentile(post_rib,5, axis=0),
             '95perc':np.percentile(post_rib,95, axis=0)}
    
        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_rib_timeseries_' + scen + '.csv')
    
    
        plot_felt = post_rib[2014]
        axs[1].hist(plot_felt,bins=bin,density=True,
                    color='darkgray',label='posteriori')
        frek, bins = np.histogram(plot_felt,bins=bin,density=True)
        axs[1].plot(bins[0:-1] +((bins[1]-bins[0])/2), frek,color='black',label='Year 2014 Mean: ' + f'{plot_felt.mean():.3g}')
    
        
        plot_felt = post_rib[2010]
        #axs[1].hist(plot_felt,bins=bin,density=True,
        #            color='darkgray',label='posteriori')
        frek, bins = np.histogram(plot_felt,bins=bin,density=True)
        axs[1].plot(bins[0:-1] +((bins[1]-bins[0])/2), frek,color='gray',label='Year 2010 Mean: ' + f'{plot_felt.mean():.3g}')
        
        plot_felt = post_rib[2000]
        frek, bins = np.histogram(plot_felt,bins=bin,density=True)
        axs[1].plot(bins[0:-1] +((bins[1]-bins[0])/2), frek,linestyle='--',color='black',label='Year 2000 Mean: ' + f'{plot_felt.mean():.3g}')
        
        axs[1].set_xlabel('W m$^{-2}$')
        axs[1].legend()
        axs[0].legend()
    
    plt.suptitle('Radiative imbalance ' + scen)
plt.show()
