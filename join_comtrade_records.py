import os
import pandas as pd
from config.config_reader import read_config
from lib import join_records

print('Join and filter COMTRADE records...')

# Settings
config = read_config()
filter_joined_by_hs6 = config.settings['filter_joined_by_hs6']
filter_joined_by_transport_mode = config.settings['filter_joined_by_transport_mode']

# Work path
work_dir = config.work_dir + str(config.year) + '/'
assert os.path.isdir(work_dir)

# Save path
save_dir = config.work_dir + 'comtrade-finished' + '/'
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Get country codes
country_iso_defs = pd.read_excel(config.data_dir + '/countries-iso-numeric-m49-conc.xlsx')
country_iso_defs = country_iso_defs.rename(columns={'M49 code': "m49_code", "ISO-alpha3 code": "iso_alpha3", 'Country or Area': 'name'})

# country_iso = country_iso_defs['m49_code'].to_list()

all_store = join_records(
    country_legend=country_iso_defs,
    year=config.year,
    work_dir=work_dir,
    save_dir=save_dir,
    filter_by_mot=filter_joined_by_transport_mode,
    filter_by_hs6=filter_joined_by_hs6,
)

# Write a copy in the legacy data format
if config.settings['mock_legacy_format']:

    print('Applying legacy format...')

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
