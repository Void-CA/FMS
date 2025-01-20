import pandas as pd 
import os
import scripts.utils as utils

fms = {
    "CAR": [],
    "CHILE": [],
    "ESP": [],
    "ARG": [],
    "MEX": [],
    "COL": [],
    "PERU": []
}

tables = os.listdir('data/raw_tables/')
for table in tables:
    df = pd.read_csv('data/raw_tables/' + table)
    df["year"] = table.split("_")[1].split(".")[0]
    df["country"] = table.split("_")[0]
    df.rename(columns={"Posición": "position"}, inplace=True)

    if not "B" in df["year"][0] and not "A" in df["year"][0]:
            df["champion"] = df["position"] == 1
    
    if "CAR_" in  table:
        fms["CAR"].append(df)

    elif "CHILE_" in table:
        fms["CHILE"].append(df)

    elif "ESP_" in table:
        fms["ESP"].append(df)

    elif "ARG_" in table:
        fms["ARG"].append(df)

    elif "MEX_" in table:
        fms["MEX"].append(df)

    elif "COL_" in table:
        fms["COL"].append(df)

    elif "PERU_" in table:
        fms["PERU"].append(df)

processed_tables = []
for country in fms.keys():
    fms_2023_corrected = utils.champion_2023(fms, country)
    fms[country].pop()
    fms[country].pop()
    fms[country].append(fms_2023_corrected)
    
    country_df = pd.concat(fms[country])
    processed_tables.append(country_df)
    country_df.to_csv(f'data/processed_tables/FMS_{country}.csv', index=False)

final_table = utils.formatting_table(processed_tables)
print(final_table.sort_values(by="PTB", ascending=False))
final_table.to_csv('data/FMS.csv', index=False)