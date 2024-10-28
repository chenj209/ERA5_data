from scipy.interpolate import RegularGridInterpolator
import numpy as np
import netCDF4 as nc

era5_data = nc.Dataset("monthly_mean.nc")
era5_lon = era5_data["longitude"][:] #1440
era5_lat = era5_data["latitude"][:]
# Define the original grid
x = era5_lat
y = era5_lon
#data = np.random.rand(721, 1440)  # Replace with your actual data
#data = np.repeat(era5_lon.reshape(1,1440), 721,axis=0)  # Replace with your actual data
data = era5_data["t2m"]  # Replace with your actual data
print(data.shape)

# Create the interpolating function
interpolating_function = RegularGridInterpolator((x, y), data)

# Define the new grid
x_new = np.linspace(-90, 90, 96)
y_new = np.linspace(0, 357.5, 144)

# Create the new grid points
x_new_grid, y_new_grid = np.meshgrid(x_new, y_new, indexing='ij')

# Interpolate data to the new grid
interpolated_data = interpolating_function((x_new_grid, y_new_grid))

print(interpolated_data.shape)  # Should print (96, 144)
print(interpolated_data[0,:])
print(interpolated_data[:,1])
