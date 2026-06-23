import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde


plt.rcParams['font.size'] = 12


filepath = '/div/qbo/utrics/ClimateSensitivity/UseCMIP6/RESULTS/'


ens_list = {'CNRM1':np.arange(1,31,1),
            'HadGEM3':np.arange(1,5,1),
            'NorESM2MM': np.arange(1,4,1),
            'NorESM2LM': np.arange(1,4,1)} 

filepath_cataloge = {'CNRM1':'postTCR_CMIP6',
                     'HadGEM3':'postTCR_CMIP6',
                     'NorESM2MM':'postTCR_CMIP6',
                     'NorESM2LM':'postTCR_CMIP6'}

model_list = ['CNRM1',
              'HadGEM3',
              'NorESM2MM',
              'NorESM2LM']
"""
model_list = ['NorESM2MM',
              'NorESM2LM']
"""

#model_list = ['CNRM1']
#ens_list = {'CNRM1':[23]}
#filepath_cataloge = {'CNRM1':'CNRM1R23'}

filename = 'postTCR.txt'

plotte = False
for model in model_list:
    for ens in ens_list[model]:
        scen = 'OutputAnalyse'+model+'R'+str(ens)
        
        post_tcr= pd.read_csv(filepath+filepath_cataloge[model]+'/'
                              +scen+'/'+filename,sep=' ',header=None)
        post_tcr = post_tcr[0]
        print(post_tcr)
        


        #######################################################
        samples = len(post_tcr.index)
        bin = (int(samples*0.001))
        if plotte:
            fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(10,8))
            
            axs.hist(post_tcr,bins=bin,density=True,
                     color='darkgray',label='posteriori '+scen)
            frek, bins = np.histogram(post_tcr,bins=bin,density=True)
            axs.plot(bins[0:-1] +((bins[1]-bins[0])/2), frek,color='black')
            
            axs.legend()
            axs.set_xlabel('K')
            axs.set_title('Transient Climate Sensisitvity')
            

        kde = gaussian_kde(post_tcr)
        print(kde)
        dist_space = np.linspace( min(post_tcr), max(post_tcr), 100 )
        print(dist_space)
        
        if plotte:
            axs.plot(dist_space,kde(dist_space),linewidth=0.5,color='blue',label='gausian_kde')
            
        print(kde(dist_space))
        print(dist_space)

        #Write to file:
        gaussian_df = pd.DataFrame(data=kde(dist_space),index=dist_space,columns=[scen])
        print(gaussian_df)
        gaussian_df.to_csv('results_csv/'+scen+'_gaussiankde_tcr.csv')


        tcr_mean = np.mean(post_tcr)
        ###
        if plotte:
            ipcc_central = 1.8
            ipcc_likely = [1.4,2.2]
            ipcc_very_likely = [1.2,2.4]
            axs.plot(ipcc_central, 0.1,'o',color='purple',label='IPCC central')
            axs.plot(ipcc_likely,[0.1,0.1], color='purple',label='IPCC likely')
            axs.plot(ipcc_very_likely,[0.1,0.1], linestyle='--',color='purple',label='IPCC very likely')
    

            left, right = axs.get_xlim()
            bottom, top= axs.get_ylim()
    
   

            axs.text(3.5,0.5*top,'TCR: '+
                     '\nMean:    '+f"{tcr_mean:.3g}" + 
                     '\nMedian:  '+f"{np.percentile(post_tcr,50):.3g}"+
                     '\n5perc:   '+f"{np.percentile(post_tcr,5):.3g}"+
                     '\n95perc:  '+f"{np.percentile(post_tcr,95):.3g}")
        



        #Write to file:
        d = {'Mean': tcr_mean,
             'Median': np.percentile(post_tcr,50),
             '5perc':np.percentile(post_tcr,5),
             '95perc':np.percentile(post_tcr,95)}
        summary_df = pd.DataFrame(data=d, index=[scen])
        summary_df.to_csv('results_csv/summary_tcr_' + scen + '.csv')
    


    if plotte:
        axs.legend()

plt.show()
