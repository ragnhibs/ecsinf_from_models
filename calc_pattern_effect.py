import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


filepath = '/div/qbo/utrics/ClimateSensitivity/UseCMIP6/RESULTS/'

#model = 'CNRM1'
#model = 'NorESM2MM'
#model = 'NorESM2LM'
model = 'HadGEM3'


ens_list = {'CNRM1':np.arange(1,31,1),
            'HadGEM3':np.arange(1,5,1),
            'NorESM2MM': np.arange(1,4,1),
            'NorESM2LM': np.arange(1,4,1)} 

filepath_cataloge = {'CNRM1':'CNRM_R1-R30',
                     'HadGEM3':'HadGEM_R1-R4',
                     'NorESM2MM':'NorESM2',
                     'NorESM2LM':'NorESM2'}

#model = 'CNRM1'
#ens_list = {'CNRM1':[23]}
#filepath_cataloge = {'CNRM1':'CNRM1R23'}





#From IPCC AR6 Table 7.2

co2x2_erf = {'CNRM1': 4.01,
             'HadGEM3': 4.07,
             'NorESM2LM':4.10,
             'NorESM2MM':4.22}


ecs_cmip6 = {'CNRM1': 4.83,
             'HadGEM3': 5.55,
             'NorESM2LM': 2.54,
             'NorESM2MM': 2.50}


print(co2x2_erf)

filename = 'post_parval.txt'

paralist_short= ['akapa', 'cpi' , 'w', 'rlamdo', 'beto', 'mixed', 'LAMBDA']
paralist = ['Vertical heat diffusivity',
            'Polar parameter',
            'Upwelling velocity',
            'Air-sea heat exchange parameter',
            'Oceanic interhemispheric heat exchange parameter',
            'Mixed layer depth',
            'Climate sensitivity']

plotte = True




for ens in ens_list[model]:
    
    scen = 'OutputAnalyse'+model+'R'+str(ens)
    post_parval= pd.read_csv(filepath+filepath_cataloge[model]+'/'
                             +scen+'/'+filename,sep=' ',header=None)

    post_parval.columns = paralist

    post_ecs_inf = post_parval['Climate sensitivity']
    
    
    pattern = 1.0/post_ecs_inf - 1.0/(ecs_cmip6[model]/co2x2_erf[model])


    #Write to file:
    d = {'Mean': np.mean(pattern),
         'Median': np.percentile(pattern,50),
         '5perc':np.percentile(pattern,5),
         '95perc':np.percentile(pattern,95)}
    summary_df = pd.DataFrame(data=d, index=[scen])
    summary_df.to_csv('results_csv/summary_pattern_' + scen + '.csv')
