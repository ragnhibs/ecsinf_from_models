import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#This is zero as only one obs timeseries are used. 

plt.rcParams['font.size'] = 8

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

filename = 'constantForDataSeries.txt'



for model in model_list:
    for ens in ens_list[model]:
        scen = 'OutputAnalyse'+model+'R'+str(ens)
        print(scen)
        constants = pd.read_csv(filepath+filepath_cataloge[model]+'/'+scen+'/'+filename,
                                sep=' ',skipinitialspace=True, header=None)

        constants.set_axis([ens],axis=1,inplace=True)
    
        constants.index =['nh', 'sh','0to700','700to2000']
                      
    
        print(constants)
        if ens == 1:
            constants_all = constants
        else:
            constants_all = pd.concat([constants_all,constants],axis=1)

    #outfile = 'results_csv/constantForDataSeries_'+scen+'.txt'
    #constants_all.to_csv(outfile)



    print(constants_all)

##
#
#
#OutputAnalyse02 (nye temperaturdata) 19 kolonner:
#	NH: giss, hadcrut, noaa, 
#	SH: giss, hadcrut, noaa,
#	_0to700: IAP_Cheng,Ishii,PMEL,OPEN-OHC,NCEI_Levitus,EN4,Domingues
#	_700to2000: IAP_Cheng,Ishii,PMEL,OPEN-OHC,NCEI_Levitus,EN4


    
