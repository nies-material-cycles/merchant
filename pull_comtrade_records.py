import pandas as pd
import comtradeapicall
from config.config_reader import read_config

# Settings
config = read_config()

# Get country codes
countries_iso_numeric = pd.read_excel(config.data_dir + '/countries-iso-numeric-m49-conc.xlsx');
country_iso = countries_iso_numeric['M49 code'].to_list()

for c in countries_iso_numeric.iterrows():

    iso_code = c[1]['M49 code']
    iso_acr = c[1]['ISO-alpha3 code']

    print('Processing: ' + iso_acr + '(' + str(iso_code) + ')')

    comtradeapicall.bulkDownloadFinalFile(
        config.subscription_key,
        config.work_dir,
        typeCode="C",
        freqCode='A',
        clCode="HS",
        period=str(config.year),
        reporterCode=iso_code,
        decompress=True,
    )

    print('.')
        
print('Finished.')
