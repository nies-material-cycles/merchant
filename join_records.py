import pandas as pd
from config.config_reader import read_config
from glob import glob
import csv

print('Join and filter COMTRADE records...')

# Settings
config = read_config()
files = [f for f in glob(config.work_dir + "*.txt")]
assert len(files) > 0

# Extract each file 
print('Extracting ' + str(len(files)) + ' files...')

store = pd.DataFrame() 
i = 0

for f in files:

    with open(f, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        df = pd.DataFrame(reader)

    # Fix the header
    header = df.iloc[0] 
    df = df[1:] 
    df.columns = header 
    df = df.reset_index(drop=True)

    # Filter
    df['motCode'] = df['motCode'].astype(int)
    df = df.loc[df['motCode'] > 0]

    df['cmdCode'] = df['cmdCode'].astype(str)
    df = df.loc[df['cmdCode'].str.len() == 6]
        
    # Append
    if df.shape[0] > 0:
        store = pd.concat([store, df], axis=0).reset_index(drop=True)

    i = i + 1
    print(str(i) + '/' + str(len(files)))

print('Joined store contains ' + '{:,.0f}'.format(store.shape[0]) + ' records.')

store.to_csv(config.work_dir + 'comtrade-joined-records' + str(config.year) + '.csv')

print('Finished.')

