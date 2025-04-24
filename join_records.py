import os
import pandas as pd
from config.config_reader import read_config
from glob import glob
import csv

print('Join and filter COMTRADE records...')

# Settings
config = read_config()
filter_joined_by_hs6 = config.settings['filter_joined_by_hs6']
filter_joined_by_transport_mode = config.settings['filter_joined_by_transport_mode']

# Save path
save_dir = config.work_dir + str(config.year) + '/'
assert os.path.isdir(save_dir)

# Get country codes
countries_iso_numeric = pd.read_excel(config.data_dir + '/countries-iso-numeric-m49-conc.xlsx');
country_iso = countries_iso_numeric['M49 code'].to_list()

store = []
m = countries_iso_numeric.shape[0]
for i, c in enumerate(countries_iso_numeric.iterrows()):

    # Meta
    iso_code = c[1]['M49 code']
    iso_acr = c[1]['ISO-alpha3 code']
    save_dir_c = save_dir + iso_acr + '/'
    
    print(' (' + str(i) + '/' + str(m) + ') ' + iso_acr + ' (' + str(iso_code) + ')')

    if os.path.isdir(save_dir_c):

        files = [f for f in glob(save_dir_c + "*.txt")]
        if len(files) == 0:
            os.rmdir(save_dir_c)
        else:
            
            # Extract files 
            assert len(files) == 1
            
            for f in files:

                with open(f, 'r') as file:
                    reader = csv.reader(file, delimiter='\t')
                    df = pd.DataFrame(reader)

                # Fix the header
                header = df.iloc[0] 
                df = df[1:] 
                df.columns = header 
                df = df.reset_index(drop=True)

                # Data types
                df['motCode'] = df['motCode'].astype(int)
                df['cmdCode'] = df['cmdCode'].astype(str)
                
                # Filter
                if filter_joined_by_transport_mode:
                    df = df.loc[df['motCode'] > 0]

                if filter_joined_by_hs6:
                    df = df.loc[df['cmdCode'].str.len() == 6]
                    
                # Country name
                df['Reporter'] = c[1]['Country or Area']


                # Append
                if df.shape[0] > 0:
                    store.append(df)

print('Joining records...')

all_store = pd.concat(store, ignore_index=True)

print('Complete store contains ' + '{:,.0f}'.format(all_store.shape[0]) + ' records.')

all_store.to_csv(save_dir + 'comtrade-joined-records-' + str(config.year) + '.csv', index=False)

if config.settings['mock_legacy_format']:

    all_store = all_store.rename(columns={"classificationCode": "Classification",
                                          "refYear": "Year",
                                          "period": "Period",
                                          "reporterCode": "Reporter ISO", 
                                          "netWgt": "Netweight (kg)"})
    
    # Missing columns
    all_store['Period Desc.'] = all_store['Period']
    all_store['Aggregate Level'] = 2 
    all_store['Is Leaf Code'] = 0

    # Set column order
    col_order = ["Classification", "Year", "Period", 'Period Desc.', 'Aggregate Level', 'Is Leaf Code', 'Trade Flow Code', 'Trade Flow',
                 "Reporter ISO", 'Netweight (kg)']
    legacy_store = all_store[col_order]

    # Write to disk
    legacy_store.to_csv(save_dir + 'comtrade-joined-records-legacy-format-' + str(config.year) + '.csv', index=False)

print('Finished.')

