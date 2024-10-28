import xarray as xr

# Load the dataset
file_path = 'output2.5-1.0_Q.grib'  # Replace with your file path, e.g., 'your_file.grib'
ds = xr.open_dataset(file_path, engine="cfgrib")

# Print the entire dataset structure
print(ds)

# Or, print just the variables and their dimensions
for var_name in ds.variables:
    variable = ds[var_name]
    print(f"Variable: {var_name}")
    print(f"Dimensions: {variable.dims}")
    print(f"Shape: {variable.shape}")
    print(f"Attributes: {variable.attrs}\n")
print(ds["latitude"])
