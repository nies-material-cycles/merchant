import os
import pandas as pd
from config.config_reader import read_config
from lib.methods import pull_records

print('Pulling COMTRADE records...')

# Settings
config = read_config()

# Save path
save_dir = config.work_dir + str(config.year) + '/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Get country codes
countries_iso_numeric = pd.read_excel(config.data_dir + '/countries-iso-numeric-m49-conc.xlsx')

# Pull from Comtrade API
pull_records(country_legend=countries_iso_numeric, auth=config.subscription_key, year=config.year, save_dir=save_dir)
        
print('Finished.')
