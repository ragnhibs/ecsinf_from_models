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

filename = 'postNoiseM.txt'

for model in model_list:
    for ens in ens_list[model]:
        scen = 'OutputAnalyse'+model+'R'+str(ens)
    

        post_noise_val= pd.read_csv(filepath+filepath_cataloge[model]+'/'+scen+'/'+filename,sep=' ',skipinitialspace=True, header=None)
        #print(post_noise_val)
    
        scip_columns = 4
        len = scip_columns + 4*antyr
        print(len)

        column_select_nh = np.arange(scip_columns+0,len+1,4)
        column_select_sh = np.arange(scip_columns+1,len+2,4)
        column_select_ohc_above700 = np.arange(scip_columns+2,len+3,4)
        column_select_ohc_below700 = np.arange(scip_columns+3,len+4,4)
    


        post_noise_nh = post_noise_val[column_select_nh]
        print(post_noise_nh)
        post_noise_nh.columns = yearlist
        print(post_noise_nh)
    
        #Posterior Write to file:
        d = {'Median': np.percentile(post_noise_nh,50, axis=0),
             '5perc':np.percentile(post_noise_nh,5, axis=0),
             '95perc':np.percentile(post_noise_nh,95, axis=0)}
    
        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_noise_temp_nh_' + scen + '.csv')

        ##############
        post_noise_sh = post_noise_val[column_select_sh]
        print(post_noise_sh)
        post_noise_sh.columns = yearlist
        print(post_noise_sh)

        #Posterior Write to file:
        d = {'Median': np.percentile(post_noise_sh,50, axis=0),
             '5perc':np.percentile(post_noise_sh,5, axis=0),
             '95perc':np.percentile(post_noise_sh,95, axis=0)}

        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_noise_temp_sh_' + scen + '.csv')


        post_noise_glob = 0.5*(post_noise_sh + post_noise_nh)
        #Posterior Write to file:
        d = {'Median': np.percentile(post_noise_glob,50, axis=0),
             '5perc':np.percentile(post_noise_glob,5, axis=0),
             '95perc':np.percentile(post_noise_glob,95, axis=0)}
    
        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_noise_temp_glob_' + scen + '.csv')




        ############
        post_noise_ohc_above_700 = post_noise_val[column_select_ohc_above700]
        print(post_noise_ohc_above_700)
        post_noise_ohc_above_700.columns = yearlist
        print(post_noise_ohc_above_700)
        
        #Posterior Write to file:
        d = {'Median': np.percentile(post_noise_ohc_above_700,50, axis=0),
             '5perc':np.percentile(post_noise_ohc_above_700,5, axis=0),
             '95perc':np.percentile(post_noise_ohc_above_700,95, axis=0)}

        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_noise_ohc_above700_' + scen + '.csv')
        
        ############
        post_noise_ohc_below_700 = post_noise_val[column_select_ohc_below700]
        print(post_noise_ohc_below_700)
        post_noise_ohc_below_700.columns = yearlist
        print(post_noise_ohc_below_700)
        
        #Posterior Write to file:
        d = {'Median': np.percentile(post_noise_ohc_below_700,50, axis=0),
             '5perc':np.percentile(post_noise_ohc_below_700,5, axis=0),
             '95perc':np.percentile(post_noise_ohc_below_700,95, axis=0)}
        
        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_posterior_noise_ohc_below700_' + scen + '.csv')



print('Done!')
