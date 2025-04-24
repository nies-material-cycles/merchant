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
country_iso_defs = pd.read_excel(config.data_dir + '/countries-iso-numeric-m49-conc.xlsx')
country_iso_defs = country_iso_defs.rename(columns={'M49 code': "m49_code", "ISO-alpha3 code": "iso_alpha3", 'Country or Area': 'name'})

country_iso = country_iso_defs['m49_code'].to_list()

# Unpack each country's file
store = []
m = country_iso_defs.shape[0]

for i, c in enumerate(country_iso_defs.iterrows()):

    # Meta
    iso_code = c[1]['m49_code']
    iso_acr = c[1]['iso_alpha3']
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
                    
                # Reporter country
                c_name = c[1]['name']
                df['Reporter'] = c_name


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
                                          "reporterCode": "Reporter Code", 
                                          "partnerCode": "Partner Code", 
                                          "cmdCode": "Commodity Code",
                                          "qty": "Qty",
                                          "qtyUnitCode": "Qty Unit Code",
                                          "netWgt": "Netweight (kg)",
                                          "primaryValue": 'Trade Value (US$)'})
    

    # Missing columns
    all_store['Period Desc.'] = all_store['Period']
    all_store['Aggregate Level'] = 2 
    all_store['Is Leaf Code'] = 0

    # Map trade flow codes
    di = {'M': 1, 'X': 2, 'RX': 3, 'RM': 4}
    all_store['Trade Flow Code'] = all_store['flowCode'].map(di).fillna(value=9).astype(int)

    di = {'M': 'Import', 'X': 'Export', 'RX': 'Re-Export', 'RM': 'Re-Import'}
    all_store['Trade Flow'] = all_store['flowCode'].map(di).fillna(value='Other')
    
    # Country codes
    c_idx_acr_map = pd.Series(country_iso_defs.iso_alpha3.values,index=country_iso_defs.m49_code.astype(str)).to_dict()
    all_store['Reporter ISO'] = all_store['Reporter Code'].map(c_idx_acr_map).fillna(value='WLD')
    all_store['Partner ISO'] = all_store['Partner Code'].map(c_idx_acr_map).fillna(value='WLD') 

    c_idx_name_map = pd.Series(country_iso_defs.name.values,index=country_iso_defs.m49_code.astype(str)).to_dict()
    all_store['Reporter'] = all_store['Reporter Code'].map(c_idx_name_map).fillna(value='World')
    all_store['Partner'] = all_store['Partner Code'].map(c_idx_name_map).fillna(value='World')

    all_store['Commodity'] = 'xx'
    all_store['Flag'] = 0

    # Quantity mapping
    qty_codes = pd.read_excel(config.data_dir + '/ComtradePlus_DataItems.xlsx', sheet_name='REF QTY')
    qty_idx_abv_map = pd.Series(qty_codes.qtyAbbr.values,index=qty_codes.qtyCode.astype(str)).to_dict()
    all_store["Qty Unit"] = all_store['Qty Unit Code'].map(qty_idx_abv_map)

    # Set column order
    col_order = ["Classification", "Year", "Period", 'Period Desc.', 'Aggregate Level', 'Is Leaf Code', 'Trade Flow Code', 'Trade Flow',
                 "Reporter Code", "Reporter", "Reporter ISO" , "Partner Code", "Partner", "Partner ISO" ,
                 "Commodity Code", "Commodity",
                 "Qty Unit Code", "Qty Unit", "Qty",
                 "Netweight (kg)", 'Trade Value (US$)', 'Flag']
    
    legacy_store = all_store[col_order]

    # Write to disk
    legacy_store.to_csv(save_dir + 'comtrade-joined-records-legacy-format-' + str(config.year) + '.csv', index=False)

print('Finished.')

