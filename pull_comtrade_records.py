import os
import pandas as pd
import comtradeapicall
from config.config_reader import read_config

print('Pulling COMTRADE records...')

# Settings
config = read_config()
continue_previous_download = config.settings['continue_previous_download']

# Save path
save_dir = config.work_dir + str(config.year) + '/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Get country codes
countries_iso_numeric = pd.read_excel(config.data_dir + '/countries-iso-numeric-m49-conc.xlsx');
country_iso = countries_iso_numeric['M49 code'].to_list()

for c in countries_iso_numeric.iterrows():

    # Meta
    iso_code = c[1]['M49 code']
    iso_acr = c[1]['ISO-alpha3 code']
    save_dir_c = save_dir + iso_acr + '/'
    
    print('Processing: ' + iso_acr + ' (' + str(iso_code) + ')')

    if not os.path.isdir(save_dir_c):

        os.mkdir(save_dir_c)

        comtradeapicall.bulkDownloadFinalFile(
            config.subscription_key,
            save_dir_c,
            typeCode="C",
            freqCode='A',
            clCode="HS",
            period=str(config.year),
            reporterCode=iso_code,
            decompress=True,
        )

    else:
        print('Records already exist')

    print('.')
        
print('Finished.')
