import os
import pandas as pd 

from config.config_reader import read_config
from lib.methods import pull_records, join_records
from lib.formatter import apply_legacy_formatting

print('Running Comtrade batch processor...')

# Settings
config = read_config()

timeseries = config.settings['timeseries']
auth = config.subscription_key

filter_by_hs6 = config.settings['filter_joined_by_hs6']
filter_by_transport_mode = config.settings['filter_joined_by_transport_mode']

# Get country codes
country_legend = pd.read_excel(config.data_dir + '/countries-iso-numeric-m49-conc.xlsx')

# Paths
save_dir = config.work_dir + 'comtrade-finished' + '/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Request each year in timeseries
for t in timeseries:

    print(' .' + str(t))

    # Scraped data write path
    work_dir = config.work_dir + str(t) + '/'
    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)

    # Pull Comtrade records from API
    pull_records(country_legend=country_legend, auth=auth, year=t, save_dir=work_dir)

    # Join individual country files together
    all_store = join_records(
        country_legend=country_legend,
        year=t,
        work_dir=work_dir,
        save_dir=save_dir,
        filter_by_mot=filter_by_transport_mode,
        filter_by_hs6=filter_by_hs6,
    )

    # Legacy formatting
    if config.settings['mock_legacy_format']:
        apply_legacy_formatting(all_store, country_legend=country_legend, year=t, data_dir=config.data_dir, save_dir=save_dir)