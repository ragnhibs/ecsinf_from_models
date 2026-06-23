import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde


plt.rcParams['font.size'] = 12


filepath = '/div/qbo/utrics/ClimateSensitivity/UseCMIP6/RESULTS/'

fullname = {'CNRM1':'CNRM-CM6-1',
            'NorESM2MM':'NorESM2MM',
            'NorESM2LM': 'NorESM2LM',
            'HadGEM3':'HadGEM3 GC3.1-LL'}


"""

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


"""

model = 'CNRM1'
ens_list = {'CNRM1':[23]}
filepath_cataloge = {'CNRM1':'CNRM1R23'}

#Smith et al 2020.
#CNRM-CM6-1 8.00
#HadGEM3-GC31-LL 8.09
#NorESM2-LM 8.15
#NorESM2-MM 8.38

#From Zelinka table S1:
#co2x2_erf = {'CNRM1': 3.64,
#             'HadGEM3': 3.49,
#             'NorESM2LM':3.44,
#             'NorESM2MM':3.44*8.38/8.15}

#print(co2x2_erf)

#For NorESM2-MM, scale with the 4xCO2 from Smith et al 2020.

#From IPCC AR6 Table 7.2
co2x2_erf = {'CNRM1': 4.01,
             'HadGEM3': 4.07,
             'NorESM2LM':4.10,
             'NorESM2MM':4.22}

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

    post_ecs_inf = post_parval['Climate sensitivity']*co2x2_erf[model]
    
    

    #######################################################
   

    if plotte:
        samples = len(post_ecs_inf.index)
        bin = (int(samples*0.001))
        fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(10,8))
        
        axs.hist(post_ecs_inf,bins=bin,density=True,
                 color='darkgray',label='posteriori '+scen)
        frek, bins = np.histogram(post_ecs_inf,bins=bin,density=True)
        axs.plot(bins[0:-1] +((bins[1]-bins[0])/2), frek,color='black')
        
        axs.legend()
        axs.set_xlabel('K')
        axs.set_title('Inferred Effective Climate Sensisitvity')
        

        
    kde = gaussian_kde(post_ecs_inf)
    print(kde)
    dist_space = np.linspace( min(post_ecs_inf), max(post_ecs_inf), 100 )
    print(dist_space)

    if plotte:
        axs.plot(dist_space,kde(dist_space),linewidth=0.5,color='blue',label='gausian_kde')

    print(kde(dist_space))
    print(dist_space)

    #Write to file:
    gaussian_df = pd.DataFrame(data=kde(dist_space),index=dist_space,columns=[scen])
    print(gaussian_df)
    gaussian_df.to_csv('results_csv/'+scen+'_gaussiankde_ecs_inf.csv')


    ecs_inf_mean = np.mean(post_ecs_inf)
    ###
    if plotte:
        
        left, right = axs.get_xlim()
        bottom, top= axs.get_ylim()
    
   

        axs.text(3.5,0.5*top,'ECS_INF: '+
                 '\nMean:    '+f"{ecs_inf_mean:.3g}" + 
                 '\nMedian:  '+f"{np.percentile(post_ecs_inf,50):.3g}"+
                 '\n5perc:   '+f"{np.percentile(post_ecs_inf,5):.3g}"+
                 '\n95perc:  '+f"{np.percentile(post_ecs_inf,95):.3g}")
        



    #Write to file:
    d = {'Mean': ecs_inf_mean,
         'Median': np.percentile(post_ecs_inf,50),
         '5perc':np.percentile(post_ecs_inf,5),
         '95perc':np.percentile(post_ecs_inf,95)}
    summary_df = pd.DataFrame(data=d, index=[scen])
    summary_df.to_csv('results_csv/summary_ecs_inf_' + scen + '.csv')
    


if plotte:
    axs.legend()

    plt.show()
