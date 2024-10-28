import cdsapi

c = cdsapi.Client()

#c.retrieve(
#    'reanalysis-era5-single-levels-monthly-means',
#    {
#        'format': 'netcdf',
#        'product_type': 'monthly_averaged_reanalysis',
#        'variable': '2m_temperature',
#        'year': [
#            '1998', '1999', '2000',
#            '2001', '2002', '2003',
#            '2004',
#        ],
#        'month': [
#            '01', '02', '03',
#            '04', '05', '06',
#            '07', '08', '09',
#            '10', '11', '12',
#        ],
#        'time': '00:00',
#    },
#    'download.nc')


c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'format': 'netcdf',
        'product_type': 'monthly_averaged_reanalysis',
        'variable': 'vertical_integral_of_temperature',
        'year': '1998',
        'month': '01',
        'time': '00:00',
    },
    'download.nc')
