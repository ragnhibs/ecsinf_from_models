import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 8


filepath = '/div/qbo/utrics/ClimateSensitivity/UseCMIP6/RESULTS/'

"""
#model_list = ['CNRM1',
#              'HadGEM3',
#              'NorESM2MM',
#              'NorESM2LM']
model_list = ['NorESM2MM',
              'NorESM2LM']


ens_list = {'CNRM1':np.arange(1,31,1),
            'HadGEM3':np.arange(1,5,1),
            'NorESM2MM': np.arange(1,4,1),
            'NorESM2LM': np.arange(1,4,1)} 

filepath_cataloge = {'CNRM1':'CNRM_R1-R30',
                     'HadGEM3':'HadGEM_R1-R4',
                     'NorESM2MM':'NorESM2',
                     'NorESM2LM':'NorESM2'}
"""

model_list = ['CNRM1']
ens_list = {'CNRM1':[23]}
filepath_cataloge = {'CNRM1':'CNRM1R23'}




year_start = 1850
year_end = 2014
antyr = year_end-year_start
yearlist = np.arange(year_start,year_end+1)


filename = 'postTempNew.txt'

for model in model_list:
    for ens in ens_list[model]:
        scen = 'OutputAnalyse'+model+'R'+str(ens)

        post_temp_val= pd.read_csv(filepath+filepath_cataloge[model]+'/'
                             +scen+'/'+filename,sep=' ',header=None)
        
    
        #NH, SH, OHC0to700, OHCbelow700
        teller=0
        for y,yr in enumerate(yearlist): 
            print(yr)
            print([teller+0,teller+1,teller+2,teller+3])
            #Initialize dataframe
            if teller == 0:
                df_NH = post_temp_val.iloc[:,teller+0]
                df_NH.name = yr
                df_NH_all = df_NH
                
                df_SH = post_temp_val.iloc[:,teller+1]
                df_SH.name = yr
                df_SH_all = df_SH
                
                df_OHCto700 = post_temp_val.iloc[:,teller+2]
                df_OHCto700.name = yr
                df_OHCto700_all = df_OHCto700
                
                df_OHCbelow700 = post_temp_val.iloc[:,teller+3]
                df_OHCbelow700.name = yr
                df_OHCbelow700_all = df_OHCbelow700
            else:    
                df_NH = post_temp_val.iloc[:,teller+0]
                df_NH.name = yr
                df_NH_all = pd.concat([df_NH_all,df_NH],axis=1)    
                
                df_SH = post_temp_val.iloc[:,teller+1]
                df_SH.name = yr
                df_SH_all = pd.concat([df_SH_all,df_SH],axis=1)    
                
                df_OHCto700 = post_temp_val.iloc[:,teller+2]
                df_OHCto700.name = yr
                df_OHCto700_all = pd.concat([df_OHCto700_all,df_OHCto700],axis=1) 
                
                df_OHCbelow700 = post_temp_val.iloc[:,teller+3]
                df_OHCbelow700.name = yr
                df_OHCbelow700_all = pd.concat([df_OHCbelow700_all,df_OHCbelow700],axis=1) 
            
            teller = teller + 4

        df_NH_all.to_csv('results_csv/post_'+scen+'_temp_NH.txt')
        df_SH_all.to_csv('results_csv/post_'+scen+'_temp_SH.txt')
        df_OHCto700_all.to_csv('results_csv/post_'+scen+'_OHCto700.txt')
        df_OHCbelow700_all.to_csv('results_csv/post_'+scen+'_OHCbelow700.txt')

        
print('Results written to file')
print('Done!')

