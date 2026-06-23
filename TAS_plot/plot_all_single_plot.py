import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm, colors
import xarray as xr
import numpy as np
import os
import cartopy.crs as ccrs
from scipy import stats

plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 300

# Define a function to calculate the linear trend
def linear_trend(x):
    n = len(x)
    t = np.arange(n)
    slope, intercept, r_value, p_value, std_err = stats.linregress(t, x)

    return slope, p_value


cmipDir = "/div/no-backup-nac/CMIP6/CMIP6_downloads/historical/tas/"


fullname = {'CNRM1':'CNRM-CM6-1',
            'NorESM2MM':'NorESM2-MM',
            'NorESM2LM': 'NorESM2-LM',
            'HadGEM3':'HadGEM3-GC31-LL'}

ens_end = {'CNRM1':'i1p1f2_gr_',
           'HadGEM3':'i1p1f3_gn_',
           'NorESM2MM':'i1p1f1_gn_',
           'NorESM2LM':'i1p1f1_gn_'}

ens_list = {'CNRM1': np.arange(1,31,1),
            'HadGEM3': np.arange(1,5,1),
            'NorESM2MM': np.arange(1,4,1),
            'NorESM2LM': np.arange(1,4,1)} 

cmap = mpl.colormaps["coolwarm"]
vmax = 0.5     #OBS, remember to set meaningfull values for
vmin = -0.5

startYear = 1980
endYear = 2014

for model in fullname:
    print(model)
    print(ens_list[model])
    
    for ens in ens_list[model]:
        print(ens)
        filename = 'tas_Amon_' +fullname[model]+'_historical_r'+str(ens)+ens_end[model]+'185001-201412.nc'
        print(filename)

            


        ds = xr.open_dataset(cmipDir+filename)
        ds = ds.sel(time=slice(str(startYear),str(endYear)))    # Select time periode
        
        ds = ds.groupby("time.year").mean()       #For yearmean
        
        tas = ds["tas"]
        
        
        
        
        
        fig,ax = plt.subplots(1,1,figsize=(6.5,5),subplot_kw={'projection': ccrs.PlateCarree()})
        
        
        trend = xr.apply_ufunc(linear_trend, tas, vectorize=True, input_core_dims=[['year']], output_core_dims=[[], []])
        slope = trend[0]*10.0 #per decade
        p_value = trend[1]
        
        
        # Define significance level
        alpha = 0.05
        
        # Plot the slope
        
        slope.plot(ax=ax, vmin=vmin, vmax=vmax,cmap='coolwarm', cbar_kwargs={'orientation': 'horizontal','label': str(startYear) +'-'+str(endYear)+' linear temperature trend [°C decade$^{-1}$]'})
        
        # Hatch areas where p-value is greater than alpha
        hatch = np.where(p_value > alpha, True, False)
        ax.contourf(slope.lon, slope.lat, hatch, levels=[0.5, 1.5], hatches=['..'], colors='none')
        ax.coastlines()
        
        plt.title('')#fullname[model] + ' r' + str(ens))
        

        print('Save fig: Fig/tastrend_' + str(startYear) + str(endYear) +'_' +fullname[model] + '_r' + str(ens)+'.png')
        plt.savefig('Fig/tastrend_' + str(startYear) + str(endYear) + '_'+fullname[model] + '_r' + str(ens)+'.png',bbox_inches='tight', pad_inches=0)

        plt.close()
