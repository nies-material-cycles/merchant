import pandas as pd

def apply_legacy_formatting(all_store, country_legend=None, year=None, data_dir=None, save_dir=None):
    """
    country_legend: ISO country definitions, Dataframe
    year: download year, int
    """

    print('Applying legacy format...')

    # Rename columns
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
    c_idx_acr_map = pd.Series(country_legend.iso_alpha3.values,index=country_legend.m49_code.astype(str)).to_dict()
    all_store['Reporter ISO'] = all_store['Reporter Code'].map(c_idx_acr_map).fillna(value='WLD')
    all_store['Partner ISO'] = all_store['Partner Code'].map(c_idx_acr_map).fillna(value='WLD') 

    c_idx_name_map = pd.Series(country_legend.name.values,index=country_legend.m49_code.astype(str)).to_dict()
    all_store['Reporter'] = all_store['Reporter Code'].map(c_idx_name_map).fillna(value='World')
    all_store['Partner'] = all_store['Partner Code'].map(c_idx_name_map).fillna(value='World')

    all_store['Commodity'] = 'xx'
    all_store['Flag'] = 0

    # Quantity mapping
    qty_codes = pd.read_excel(data_dir + '/ComtradePlus_DataItems.xlsx', sheet_name='REF QTY')
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
    legacy_store.to_csv(save_dir + 'comtrade-joined-records-legacy-format-' + str(year) + '.csv', index=False)