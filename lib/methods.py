import os
from glob import glob
import csv
import pandas as pd
import comtradeapicall

def pull_records(country_legend=None, auth=None, year=None, save_dir=None):
    """
    country_legend: ISO country definitions, Dataframe
    auth: Comtrade API key, string
    year: download year, int
    save_dir: save directory, string
    """

    for c in country_legend.iterrows():

        # Country meta
        iso_code = c[1]['M49 code']
        iso_acr = c[1]['ISO-alpha3 code']

        # Save directory
        save_dir_c = save_dir + iso_acr + '/'
        
        print('Processing: ' + iso_acr + ' (' + str(iso_code) + ')')

        # Download if the country directory does not already exist
        if not os.path.isdir(save_dir_c):

            os.mkdir(save_dir_c)

            comtradeapicall.bulkDownloadFinalFile(
                auth,
                save_dir_c,
                typeCode="C",
                freqCode='A',
                clCode="HS",
                period=str(year),
                reporterCode=iso_code,
                decompress=True,
            )

        else:
            print('Records already exist')

        print('.')


def join_records(country_legend=None, year=None, work_dir=None, save_dir=None, filter_by_mot=False, filter_by_hs6=False):
    """
    country_legend: ISO country definitions, Dataframe
    year: download year, int
    work_dir: work directory, location of scraped files, string
    save_dir: save directory, string
    """

    # Rename legend columns
    country_legend = country_legend.rename(columns={'M49 code': "m49_code", 
                                                "ISO-alpha3 code": "iso_alpha3",
                                                'Country or Area': 'name'})
    # Unpack each country's file
    store = []
    m = country_legend.shape[0]

    for i, c in enumerate(country_legend.iterrows()):

        # Meta
        iso_code = c[1]['m49_code']
        iso_acr = c[1]['iso_alpha3']
        save_dir_c = work_dir + iso_acr + '/'
        
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
                    if filter_by_mot:
                        df = df.loc[df['motCode'] > 0]

                    if filter_by_hs6:
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

    all_store.to_csv(save_dir + 'comtrade-joined-records-' + str(year) + '.csv', index=False)

    return all_store