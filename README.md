# Merchant
Scrapes data from the Comtrade API gently, avoids hitting the 2.5 million row per request limit

## Methods
 `pull_comtrade_records`
 Pulls Comtrade records for a single year by country from the Comtrade API.

`join_comtrade_records`
 Joins each country's records into a single file for a single year.

 `batch_processor`
 Pulls and joins records for all years in a specified timeseries, i.e. in the config file `timeseries=[2020, 2021]`.


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

## COMTRADE specs

### Trade flow codes
| flwCode | flwDescription                           |
|---------|------------------------------------------|
| FM      | Foreign Import                           |
| M       | Import                                   |
| MIP     | Import of goods for inward processing    |
| MOP     | Import of goods after outward processing |
| RM      | Re-import                                |
| DX      | Domestic Export                          |
| RX      | Re-export                                |
| X       | Export                                   |
| XIP     | Export of goods after inward processing  |
| XOP     | Export of goods for outward processing   |

## Quantity codes

| qtyCode | qtyAbbr      | qtyDescription                                   |
|---------|--------------|--------------------------------------------------|
| -1      | N/A          | Not available or not specified or no quantity.   |
| 2       | m²           | Area in square meters                            |
| 3       | 1000 kWh     | Electrical energy in thousands of kilowatt-hours |
| 4       | m            | Length in meters                                 |
| 5       | u            | Number of items                                  |
| 6       | 2u           | Number of pairs                                  |
| 7       | l            | Volume in liters                                 |
| 8       | kg           | Weight in kilograms                              |
| 9       | 1000u        | Thousand of items                                |
| 10      | U (jeu/pack) | Number of packages                               |
| 11      | 12u          | Dozen of items                                   |
| 12      | m³           | Volume in cubic meters                           |
| 13      | carat        | Weight in carats                                 |
| 14      | km           | Length in Kilometers                             |
| 15      | g            | Weight in grams                                  |
| 16      | hive         | Beehive                                          |
| 17      | 1000 m³      | Volume in thousand cubic meters                  |
| 18      | TJ           | Terajoule (gross calorific value)                |
| 19      | BBL          | Barrels                                          |
| 20      | 1000 L       | Volume in thousands of liters                    |
| 21      | 1000 KG      | Weight in thousand of kilograms                  |
| 22      | kWH          | Electrical energy in kilowatt-hours              |
| 23      | l alc 100%   | Litre pure (100 %) alcohol - l alc. 100%         |
| 24      | head         | Head                                             |
| 25      | kg/net eda   | Kilogram drained net weight                      |
| 26      | kg C5H14ClNO | Kilogram of choline chloride                     |
| 27      | kg P2O5      | Kilogram of diphosphorus pentaoxide              |
| 28      | kg H2O2      | Kilogram of hydrogen peroxide                    |
| 29      | kg met.am.   | Kilogram of methylamines                         |
| 30      | kg N         | Kilogram of nitrogen                             |
| 31      | kg KOH       | Kilogram of potassium hydroxide (caustic potash) |
| 32      | kg K2O       | Kilogram of potassium oxide                      |
| 33      | kg NaOH      | Kilogram of sodium hydroxide (caustic soda)      |
| 34      | kg 90% sdt   | Kilogram of substance 90 % dry                   |
| 35      | kg U         | Kilogram of uranium                              |
| 36      | ct/l         | Carrying capacity in tonnes                      |
| 37      | Bq           | Becquerels                                       |
| 38      | gi F/S       | Gram of fissile isotopes                         |
| 39      | GRT          | Gross register ton                               |
| 40      | GT           | Gross tonnage                                    |
| 41      | ce/el        | Number of cells/elements                         |

## Legacy format
To structure the joined data files in the legacy format, set `mock_legacy_format=1` in the config file.

```
'Classification',
'Year',
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

Note the following fields are mocked: `Aggregate Level`, `Is Leaf Code`, `Flag`.