import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm


plotmap = False

#ens_list = ['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10',
#ens_list = ['r11','r12','r13','r14','r15','r16','r17','r18','r19','r20',
#            'r21','r22','r23','r24','r25','r26','r27','r28','r29','r30']
#model = 'CNRM-CM6-1'
#endname = 'i1p1f2_gr_'

#ens_list = ['r1','r2','r3','r4','r5']
#model = 'HadGEM3-GC31-LL'
#endname = 'i1p1f3_gn_'

ens_list = ['r1','r2','r3']
#model = 'NorESM2-LM'
model = 'NorESM2-MM'
endname= 'i1p1f1_gn_'
filepath = '/div/no-backup-nac/CMIP6/CMIP6_downloads/historical/psl/'


#filepath = '/div/no-backup/CMIP6/CMIP6_downloads/historical/psl/'
# psl:standard_name = "air_pressure_at_mean_sea_level" ;
darwin = [-12.47, 130.85]
tahiti = [-17.66, 360-149.42]

for ens in ens_list :

    filename = 'psl_Amon_'+model+'_historical_'+ens+endname+'185001-201412.nc'

    data = xr.open_dataset(filepath+filename)
    print(data)
    print(data.time)
    
    data['psl'] = data['psl']*0.01 #Pa -> hPa

    
    #Plot the two sites on a map:
    if plotmap:
        cmap = plt.get_cmap('BuPu')
        plotfield = data['psl'].isel(time=1)
        print(plotfield)
        plt.figure(figsize=(10,5))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='k')
        
        plotfield.plot(ax=ax,cmap=cmap,transform=ccrs.PlateCarree())
        
        ax.plot(darwin[1],darwin[0],'*',transform=ccrs.PlateCarree())
        ax.plot(tahiti[1],tahiti[0],'*',transform=ccrs.PlateCarree())
        
        
    #Extract pressure fields at the two sites
    darwin_psl = data['psl'].sel(lat=darwin[0],lon=darwin[1], method="nearest")
    tahiti_psl = data['psl'].sel(lat=tahiti[0],lon=tahiti[1], method="nearest")


    Pdiff = tahiti_psl - darwin_psl

    print(Pdiff)
   

    
    if plotmap:
        fig,axs = plt.subplots(nrows=2,ncols=1,figsize=(10,5))
        darwin_psl.plot(ax=axs[0],linewidth=0.2)
        tahiti_psl.plot(ax=axs[0],linewidth=0.2)
        Pdiff.plot(ax=axs[1],linewidth=0.2)
    

    #Initialize output field:
    column_name = ['Jan','Feb','Mar','Apr','May',
                   'Jun','Jul','Aug','Sep','Oct',
                   'Nov','Dec']
    yearlist = np.arange(1850,2015,1)
    df_output = pd.DataFrame(data=[],columns=column_name,index=yearlist)
    df_output.index.name='Year'
    print(df_output)
    
    
    #http://www.bom.gov.au/climate/enso/soi/
    if model == 'HadGEM3-GC31-LL':
        Pdiff_clim = Pdiff.sel(time=slice("1933-01-16","1992-12-16"))
    elif model == 'NorESM-LM':
        print(Pdiff.time)
        exit()
    
    else:
        Pdiff_clim = Pdiff.sel(time=slice("1933-01-01","1992-12-31"))

    monMean = Pdiff_clim.groupby("time.month").mean()
    monStd = Pdiff_clim.groupby("time.month").std()


    print(monMean)
    print(monStd)


    #test = Pdiff_clim.values
    #mars = test[2::12]
    #print(np.mean(mars))

    
    
    test = Pdiff.values*0.01
    for mnd in np.arange(0,12):
        group = Pdiff.groupby("time.month")
        print(group.groups)
        print(group[mnd+1])
        val = group[mnd+1]
        
        print(val)
        print(monMean[mnd])
        print(monStd[mnd])
        
        #SOI = 10 *(Pdiff - Pdiffav)/SD(Pdiff)
        soi_mnd = 10*(val.values - monMean[mnd].values)/monStd[mnd].values
    
        df_output[column_name[mnd]]= soi_mnd              
    

    print(df_output)

    df_output.to_csv(model + '_' + ens +
                     '_cmip6_soi.csv')

plt.show()
exit()


