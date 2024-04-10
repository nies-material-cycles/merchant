# Merchant
Scrapes data from the Comtrade API gently, avoids hitting the 2.5 million row per request limit

## Config
Define a `config.json` file in `/config/` directory.

```
{
    "subscription_key": "xxx",
    "year": 2022
}
```

## Environment
Requires environment variables:
```
DATA_DIR=/.../
WORK_DIR=/.../
```
where `WORK_DIR` specifies an output directory and `DATA_DIR` a directory containing the ISO M49 country definitions (countries-iso-numeric-m49-conc.xlsx).