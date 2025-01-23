import pandas as pd

def join_groups(fms:dict, country:str)->pd.DataFrame:
    group_a =  fms[country][-2]
    group_b = fms[country][-1]
    
    joined_groups = pd.concat([group_a, group_b]).sort_values(by='PTS', ascending=False)
    joined_groups = joined_groups.reset_index(drop=True)
    return joined_groups

def champion_2023(fms:dict, country:str)->pd.DataFrame:
    champions_2023 ={"ESP": "Gazir",
                     "ARG": "Larrix",
                     "CHILE": "El Menor",
                     "MEX": "Lobo Estepario",
                     "PERU": "Skill",
                     "COL": "Valles - T",
                     "CAR": "Letra"}
    fms_2023 = join_groups(fms, country)
    fms_2023["champion"] = fms_2023["MC"] == champions_2023[country]

    
    return fms_2023

def formatting_table(processed_tables:list)->pd.DataFrame:

    final_table = pd.concat(processed_tables)
    final_table["PTB"] = final_table["PTB"].apply(lambda x: str(x).replace(",", ".")).astype(float)

    # Urban Roosters got some errors in the PTB column, im using the values from another website to fix it
    corrections = {
    ("Bnet", "2020"): 2791.5,
    ("Zasko", "2020"): 2566.5,
    ("Khan", "2020"): 1986.5,
    ("Mr. Ego", "2020"): 2346.5,
    ("New Era", "2020"): 2419.5,
    ("Choque", "2020"): 2287.5,
    ("Nekroos", "2020"): 2527.5
    }   

    
    # Apply corrections
    for (mc, year), value in corrections.items():
        mask = (final_table["MC"].str.strip().str.lower() == mc.lower()) & (final_table["year"] == year)
        print(mask.any())
        if mask.any():  # Check if there are rows to update
            final_table.loc[mask, "PTB"] = value
    
    return final_table

