import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde

plt.rcParams['font.size'] = 8
#For NorESM:
rf_dict= {'Tot':[''],
          'VAL':['VAL'],
          'Rest':['_REST'],
          'Nat':['_NAT'],
          'GHG':['_GHG'],
          'AER':['_AER'],
          'LANDUSE':['_LANDUSE'],
          'O3':['_O3'],
          'aero':['aero'],
          'antro':['antro']}

#For HadGEM and CNRM
"""
rf_dict= {'Tot':[''],
          'VAL':['VAL'],
          'Rest':['_REST'],
          'Nat':['_NAT'],
          'GHG':['_GHG'],
          'AER':['_AER'],
          'aero':['aero'],
          'antro':['antro']}
"""

filepath = '/div/qbo/utrics/ClimateSensitivity/UseCMIP6/RESULTS/'

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


year_end = 2014
year_start = 1849

antyr = year_end - year_start
yearlist = np.arange(year_start,year_end+1,1)

filename_prior = 'priorRF'

print(rf_dict.keys())
rf_list=list(rf_dict.keys())


#posteriori_summary = np.zeros((len(rf_dict),4))

for model in model_list:
    ens=1
    scen = 'OutputAnalyse'+model+'R'+str(ens)
    for rf_nr,rf_comp in enumerate(rf_dict):

        print(len(rf_dict[rf_comp]))
    
        for cm,comp in enumerate(rf_dict[rf_comp]):
            fname_prior = filepath + filepath_cataloge[model]+'/'+scen +'/'+filename_prior+comp +'.txt'

            prior_rf= pd.read_csv(fname_prior,sep=' ',header=None)
        
            prior_rf_nh = prior_rf.loc[:,0:antyr]
            prior_rf_nh.columns = yearlist
        
            prior_rf_sh = prior_rf.loc[:,antyr+1:antyr+1+antyr]
            prior_rf_sh.columns = yearlist

            if cm == 0:
                prior_rf_glob = 0.5*(prior_rf_sh + prior_rf_nh)
            else:
                prior_rf_glob = prior_rf_glob + 0.5*(prior_rf_sh + prior_rf_nh)

        #Priorerior Write to file:
        d = {'Median': np.percentile(prior_rf_glob,50, axis=0),
             '5perc':np.percentile(prior_rf_glob,5, axis=0),
             #'10perc':np.percentile(prior_rf_glob,10, axis=0),
             #'20perc':np.percentile(prior_rf_glob,20, axis=0),
             #'30perc':np.percentile(prior_rf_glob,30, axis=0),
             #'40perc':np.percentile(prior_rf_glob,40, axis=0),
             #'60perc':np.percentile(prior_rf_glob,60, axis=0),
             #'70perc':np.percentile(prior_rf_glob,70, axis=0),
             #'80perc':np.percentile(prior_rf_glob,80, axis=0),
             #'90perc':np.percentile(prior_rf_glob,90, axis=0),
             '95perc':np.percentile(prior_rf_glob,95, axis=0)}
        
        summary_df = pd.DataFrame(data=d, index=yearlist)
        summary_df.to_csv('results_csv/summary_rf_prior_timeseries_all_perc_'+ rf_comp + scen + '.csv')
