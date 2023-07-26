##########################################
###  Analysis on Spotify account data  ### 
##########################################

import os
import json
import pandas as pd

def get_all_data():
    df = pd.DataFrame()

    for file in os.listdir("MyData"):
        if file.startswith("Streaming_History_Audio") and file.endswith(".json"):
            df = pd.concat([df, pd.read_json(f"MyData/{file}")])

    return df

#######################################
### Save the analysis to a txt file ###
#######################################
if __name__ == "__main__":
    print(get_all_data())
