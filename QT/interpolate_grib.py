import xarray as xr
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from tqdm.autonotebook import tqdm

# Load the GRIB file using cfgrib
grib_file = 'output2.5-1.0_Q.grib'
ds = xr.open_dataset(grib_file, engine='cfgrib')
for var_name in ds.variables:
    variable = ds[var_name]
    print(f"Variable: {var_name}")
    print(f"Dimensions: {variable.dims}")
    print(f"Shape: {variable.shape}")
    print(f"Attributes: {variable.attrs}\n")

# Extract the variables (assuming variable names 'latitude', 'longitude', 'level', and 't2m')
time = ds['time']
latitude = ds['latitude']
longitude = ds['longitude']
pressure_levels = ds['isobaricInhPa']  # Replace 'level' with the actual vertical level variable name
variable_data = ds['q']  # Replace 't2m' with the actual variable name

# New latitude, longitude, and vertical levels grids
new_latitude = np.linspace(-90, 90, 96)
new_longitude = np.linspace(0, 357.5, 144)
new_pressure_levels = np.array([3.64346569, 7.59481965, 14.35663225, 24.61222, 38.26829977,
                                54.59547974, 72.01245055, 87.82123029, 103.31712663, 121.54724076,
                                142.99403876, 168.22507977, 197.9080867, 232.82861896, 273.91081676,
                                322.24190235, 379.10090387, 445.9925741, 524.68717471, 609.77869481,
                                691.38943031, 763.40448111, 820.85836865, 859.53476653, 887.02024892,
                                912.64454694, 936.19839847, 957.48547954, 976.32540739, 992.55609512])

# Create a meshgrid for the new latitude, longitude, and vertical levels
new_plev, new_lat, new_lon = np.meshgrid(new_pressure_levels, new_latitude, new_longitude, indexing='ij')

# Initialize an array to store the interpolated data
new_data = np.empty((len(time), len(new_pressure_levels), len(new_latitude), len(new_longitude)))

# Loop over each time step and interpolate the data
for i in tqdm(range(len(time))):
    # Prepare the interpolator
    interpolating_function = RegularGridInterpolator(
        (pressure_levels, latitude, longitude), variable_data[i].values, method='linear', bounds_error=False, fill_value=np.nan
    )

    # Perform the interpolation
    new_data[i] = interpolating_function((new_plev, new_lat, new_lon))

# Create a new xarray dataset with the interpolated data
new_ds = xr.Dataset(
    {
        'Q': (['time', 'level', 'latitude', 'longitude'], new_data)
    },
    coords={
        'time': time,
        'latitude': new_latitude,
        'longitude': new_longitude,
        'level': new_pressure_levels
    }
)

# Save the new dataset to a NetCDF file
new_ds.to_netcdf('interpolated_file_with_levels.nc')
