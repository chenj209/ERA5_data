import xarray as xr
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from tqdm.autonotebook import tqdm

# Load the NetCDF file
#nc_file = 'era5_total_precip.nc'
nc_file = 'era5_mean_tp_rate.nc'
ds = xr.open_dataset(nc_file)

time_range = len(ds['date'])
# Extract the variables
date = ds['date'][:time_range]
time = pd.to_datetime(date.astype(str), format='%Y%m%d')
print(time)
latitude = ds['latitude']
longitude = ds['longitude']
#tp = ds['tp']
tp = ds['mtpr']

# Create the new latitude and longitude grids
new_latitude = np.linspace(-90, 90, 96)
new_longitude = np.linspace(0, 357.5, 144)

# Create a meshgrid for the original and new grids
original_lon, original_lat = np.meshgrid(longitude, latitude)
new_lon, new_lat = np.meshgrid(new_longitude, new_latitude)

# Initialize an array to store the interpolated data
new_tp = np.empty((time_range, len(new_latitude), len(new_longitude)))

# Loop over each time step and interpolate the data
for i in tqdm(range(time_range)):
    # Flatten the original grid and data
    original_points = np.array([original_lon.flatten(), original_lat.flatten()]).T
    original_values = tp[i].values.flatten()

    # Perform the interpolation
    new_values = griddata(original_points, original_values, (new_lon, new_lat), method='linear')

    # Store the interpolated data
    new_tp[i, :, :] = new_values

np.save("interpolated_precip.npy", new_tp)

# Create a new xarray dataset with the interpolated data
new_ds = xr.Dataset(
    {
        'tp': (['time', 'latitude', 'longitude'], new_tp)
    },
    coords={
        'time': time,
        'latitude': new_latitude,
        'longitude': new_longitude
    }
)

# Save the new dataset to a NetCDF file
new_ds.to_netcdf('interpolated_tp_rate.nc')
