################################################################
###         Analysis on Spotify account extended data        ### 
###                                                          ###
###  https://github.com/AcevedoJetter/spotify-data-analysis  ###
################################################################

import os
import time
import pandas as pd

def get_all_data():
    """
    Returns:
        df: pandas DataFrame with columns specified in the README.md
    """
    df = pd.DataFrame()

    for file in os.listdir("MyData"):
        if file.startswith("Streaming_History_Audio") and file.endswith(".json"):
            df = pd.concat([df, pd.read_json(f"MyData/{file}")])

    return df


def save_data_csv():
    """
    Saves the data in the json files to a big csv file
    """
    return get_all_data().to_csv("data.csv", index=False)


def most_streamed_artist_time(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with artist and decending order of time played in ms
    """
    data = data[["master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False)["ms_played"].sum()
    new_data = new_data.sort_values(["ms_played", "master_metadata_album_artist_name"], ascending=[False, True])
    return new_data


def most_streamed_artist_amount(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with artist and decending order of amount of songs played
    """
    data = data[["master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False).count()
    new_data = new_data.rename(columns={"ms_played" : "times_played"})
    new_data = new_data.sort_values(["times_played", "master_metadata_album_artist_name"], ascending=[False, True])
    return new_data


def most_streamed_song_time(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with song, artist, and decending order of time played in ms
    """
    data = data[["master_metadata_track_name", "master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False)["ms_played"].sum()
    new_data = new_data.sort_values(["ms_played", "master_metadata_track_name", "master_metadata_album_artist_name"], ascending=[False, True, True])
    return new_data


def most_streamed_song_amount(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with song, artist and decending order of amount played
    """
    data = data[["master_metadata_track_name", "master_metadata_album_artist_name", "ms_played"]]
    new_data = data.groupby(["master_metadata_track_name", "master_metadata_album_artist_name"], 
                                            as_index=False, 
                                            dropna=False).count()
    new_data = new_data.rename(columns={"ms_played" : "times_played"})
    new_data = new_data.sort_values(["times_played", "master_metadata_track_name", "master_metadata_album_artist_name"], ascending=[False, True, True])
    return new_data


def shuffle_offline_ratio(data, column_name):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
        column_name: should be either of 'shuffle' or 'offline'
    
    Returns:
        list: list with the percent of the string in column_name to non string of column_name songs
    """
    if column_name == "shuffle" or column_name == "offline":
        df = data.groupby(data[column_name])[column_name].count()
        true = df[True]
        false = df[False]
        total = true + false
        return [(true/total*100).round(2), (false/total*100).round(2)]
    
    return f"In the column_name parameter, you entered {column_name} insted of 'shuffle' or 'offline'"


def most_streamed_time_by_day(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        new_data: pandas DataFrame with days and decending order of time played in ms
    """
    data = data[["ts", "ms_played"]]
    for i, row in data["ts"].items():
        day = row.split("T")[0]
        data.loc[i, "ts"] = day

    new_data = data.groupby(["ts"], as_index=False, dropna=False)["ms_played"].sum()
    new_data = new_data.sort_values(["ms_played", "ts"], ascending=[False, True])
    
    return new_data


#######################################
### Save the analysis to a txt file ###
#######################################
if __name__ == "__main__":
    start = time.time()

    # Get the data from json files and turn it to a pandas DataFrame
    data = get_all_data()

    print(most_streamed_time_by_day(data))

    # Print total time to run
    print(f"Total Time in Seconds to Run File: {time.time() - start}")
