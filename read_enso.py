import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 8

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
model_list = ['NorESM2MM',
              'NorESM2LM']
"""
model_list = ['CNRM1']
ens_list = {'CNRM1':[23]}
filepath_cataloge = {'CNRM1':'CNRM1R23'}




year_start = 1850
year_end = 2014

antyr = year_end-year_start
yearlist = np.arange(year_start,year_end+1)


for model in model_list:
    for ens in ens_list[model]:
        scen = 'OutputAnalyse'+model+'R'+str(ens)

        filename = 'postBeta1NhElNino.txt'    
        post_elnino_nh= pd.read_csv(filepath+filepath_cataloge[model]+'/'+scen+'/'+filename,sep=' ',skipinitialspace=True, header=None)
        post_elnino_nh = post_elnino_nh.loc[:,0:antyr]
        post_elnino_nh.columns = yearlist
        #print(post_elnino_nh)
    
        #Posterior Write to file:
        d = {'Median': np.percentile(post_elnino_nh,50, axis=0),
             '5perc':np.percentile(post_elnino_nh,5, axis=0),
             '95perc':np.percentile(post_elnino_nh,95, axis=0)}

        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_elnino_nh_' + scen + '.csv')

        #Southern Hemisphere
        filename = 'postBeta1ShElNino.txt'

        post_elnino_sh= pd.read_csv(filepath+filepath_cataloge[model]+'/'+scen+'/'+filename,sep=' ',skipinitialspace=True, header=None)
        post_elnino_sh = post_elnino_sh.loc[:,0:antyr]
        post_elnino_sh.columns = yearlist
        print(post_elnino_sh)
    
        #Posterior Write to file:
        d = {'Median': np.percentile(post_elnino_sh,50, axis=0),
             '5perc':np.percentile(post_elnino_sh,5, axis=0),
             '95perc':np.percentile(post_elnino_sh,95, axis=0)}
        
        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_elnino_sh_' + scen + '.csv')


        post_elnino_glob = 0.5*(post_elnino_sh + post_elnino_nh)
        #Posterior Write to file:
        d = {'Median': np.percentile(post_elnino_glob,50, axis=0),
             '5perc':np.percentile(post_elnino_glob,5, axis=0),
             '95perc':np.percentile(post_elnino_glob,95, axis=0)}
        
        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_elnino_glob_' + scen + '.csv')

exit()
