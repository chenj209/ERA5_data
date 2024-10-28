import xarray as xr
import pandas as pd

# Load the NetCDF file
ds = xr.open_dataset('download.nc')

# Assuming the time variable is named 'time'
# Convert the time from "hours since 1900-01-01" to datetime objects
#time_units = 'hours since 1900-01-01 00:00:00'
#ds['time'] = pd.to_datetime(ds['time'].values, unit='h', origin=pd.Timestamp('1900-01-01'))

# Resample to monthly mean
#ds_monthly_mean = ds.resample(time='M').mean()
ds_monthly_mean = ds.resample(time='M').mean().assign_coords(time=ds['time'].resample(time='M').first())

# Save the monthly mean data to a new NetCDF file
ds_monthly_mean.to_netcdf('monthly_mean.nc')
