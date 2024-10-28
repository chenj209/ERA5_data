import xarray as xr
import numpy as np
from scipy.interpolate import griddata
from tqdm.autonotebook import tqdm

# Load the NetCDF file
nc_file = 'monthly_mean.nc'
ds = xr.open_dataset(nc_file)

# Extract the variables
time = ds['time']
latitude = ds['latitude']
longitude = ds['longitude']
t2m = ds['t2m']

# Create the new latitude and longitude grids
new_latitude = np.linspace(-90, 90, 96)
new_longitude = np.linspace(0, 357.5, 144)

# Create a meshgrid for the original and new grids
original_lon, original_lat = np.meshgrid(longitude, latitude)
new_lon, new_lat = np.meshgrid(new_longitude, new_latitude)

# Initialize an array to store the interpolated data
new_t2m = np.empty((len(time), len(new_latitude), len(new_longitude)))

# Loop over each time step and interpolate the data
for i in tqdm(range(len(time))):
    # Flatten the original grid and data
    original_points = np.array([original_lon.flatten(), original_lat.flatten()]).T
    original_values = t2m[i].values.flatten()

    # Perform the interpolation
    new_values = griddata(original_points, original_values, (new_lon, new_lat), method='linear')

    # Store the interpolated data
    new_t2m[i, :, :] = new_values

# Create a new xarray dataset with the interpolated data
new_ds = xr.Dataset(
    {
        't2m': (['time', 'latitude', 'longitude'], new_t2m)
    },
    coords={
        'time': time,
        'latitude': new_latitude,
        'longitude': new_longitude
    }
)

# Save the new dataset to a NetCDF file
new_ds.to_netcdf('interpolated_file.nc')
