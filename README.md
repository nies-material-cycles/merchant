# Merchant
Scrapes data from the Comtrade API gently, avoids hitting the 2.5 million row per request limit

## Setup
### Config
Define a `config.json` file in `/config/` directory.

```
{
    "subscription_key": "xxx",
    "year": 2022
}
```

### Environment
Requires environment variables:
```
DATA_DIR=/.../
WORK_DIR=/.../
```
where `WORK_DIR` specifies an output directory and `DATA_DIR` a directory containing the ISO M49 country definitions (countries-iso-numeric-m49-conc.xlsx).

## Legacy format
mock_legacy_format
```
Classification',
Year',
'Period',
'Period Desc.',
'Aggregate Level', 
'Is Leaf Code', 
'Trade Flow Code', 
'Trade Flow', 
'Reporter Code'  
'Reporter'
'Reporter ISO'
'Partner Code'
'Partner'
'Partner ISO'
'Commodity Code'
'Commodity'
'Qty Unit Code'
'Qty Unit'
'Qty'
'Netweight (kg)'
'Trade Value (US$)'
'Flag'
```