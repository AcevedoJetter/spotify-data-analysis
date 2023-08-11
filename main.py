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


def total_time(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        times: list with time in seconds, minutes, hours, and days
    """
    milliseconds_series = data["ms_played"]
    milliseconds = milliseconds_series.sum()
    seconds = milliseconds/1000
    minutes = seconds/60
    hours = minutes/60
    days = hours/24

    return [seconds.round(2), minutes.round(2), hours.round(2), days.round(2)]


def most_streamed_artist_time(data, top=None):
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

    if top:
        return new_data.head(top)
    return new_data


def most_streamed_artist_amount(data, top=None):
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
    
    if top:
        return new_data.head(top)
    return new_data


def most_streamed_song_time(data, top=None):
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
    
    if top:
        return new_data.head(top)
    return new_data


def most_streamed_song_amount(data, top=None):
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
    
    if top:
        return new_data.head(top)
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


def reason_start_end_ratio(data, reason):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        amounts: dictionary with the reason as key and percent of reason as value
    """
    if reason == "reason_start" or reason == "reason_end":
        data = data[reason]
        total = len(data)
        amounts = {}
        for i, row in data.items():
            if row not in amounts:
                amounts[row] = 1
            else:
                amounts[row] += 1
        for key in amounts:
            amounts[key] /= (total*1/100)
        return amounts
    
    return f"In the reason parameter, you entered {reason} insted of 'reason_start' or 'reason_end'"


def create_and_write_txt(data):
    """
    Parameters:
        data: pandas DataFrame with columns specified in the README.md
    
    Returns:
        string: will say that the txt file has been created
    """
    file = open("analysis.txt", "w")

    total_time_account = total_time(data)

    def get_top_five(data, func, top=5):
        string = ""
        info = func(data, top)
        columns = list(info.columns)
        for i in range(top):
            if func == most_streamed_artist_time:
                string += f"\t{i+1}. {info.iloc[i][columns[0]]} for a total time of {(info.iloc[i][columns[1]]/3600000).round(2)} hours\n"
            elif func == most_streamed_artist_amount:
                string += f"\t{i+1}. {info.iloc[i][columns[0]]} for a total amount of {info.iloc[i][columns[1]]} songs\n"
            elif func == most_streamed_song_time:
                string += f"\t{i+1}. {info.iloc[i][columns[0]]} by {info.iloc[i][columns[1]]} for a total time of {(info.iloc[i][columns[2]]/3600000).round(2)} hours\n"
            elif func == most_streamed_song_amount:
                string += f"\t{i+1}. {info.iloc[i][columns[0]]} by {info.iloc[i][columns[1]]} for a total amount of {info.iloc[i][columns[2]]} streams\n"
        return string
    
    shuffle = shuffle_offline_ratio(data, "shuffle")
    offline = shuffle_offline_ratio(data, "offline")

    def reason_start_end_to_string(data, reason):
        string = ""
        info = reason_start_end_ratio(data, reason)
        info_sorted = dict(sorted(info.items(), key=lambda x:x[1])[::-1])
        for reason in info_sorted:
            string += f"\n\t{reason}: {round(info[reason], 2)}"
        return string

    file.writelines([
        "SPOTIFY DATA ANALYSIS\n\n",
        f"Total Time Listened: {total_time_account[0]} seconds = {total_time_account[1]} minutes = {total_time_account[2]} hours = {total_time_account[3]} days\n\n",
        f"Most Streamed Artist by time:\n{get_top_five(data, most_streamed_artist_time)}\n",
        f"Most Streamed Artist by songs played:\n{get_top_five(data, most_streamed_artist_amount)}\n",
        f"Most Streamed Songs by time played:\n{get_top_five(data, most_streamed_song_time)}\n",
        f"Most Streamed Songs by amount of times played:\n{get_top_five(data, most_streamed_song_amount)}\n",
        f"Percent of songs on shuffle: {shuffle[0]}\nPercent of songs not on shuffle: {shuffle[1]}\n\n",
        f"Percent of songs played offline: {offline[0]}\nPercent of songs online: {offline[1]}\n\n",
        f"Reasons a song started:{reason_start_end_to_string(data, 'reason_start')}\n\n"
        f"Reasons a song ended:{reason_start_end_to_string(data, 'reason_end')}"
    ])

    file.close()

    return f"\nThe file analiysis.txt has been created and saved in the following directory: {os.getcwd()}\n"


#######################################
### Save the analysis to a txt file ###
#######################################
if __name__ == "__main__":
    start = time.time()

    # Get the data from json files and turn it to a pandas DataFrame
    data = get_all_data()

    # Save the analysis to a txt file
    print(create_and_write_txt(data))

    # Print total time to run
    print(f"Total Time in Seconds to Run File: {time.time() - start}\n")
