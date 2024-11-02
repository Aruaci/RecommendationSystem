import os
import json
import pandas as pd

directory = "./JSON_Data"

data_list = []

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename), 'r') as file:
            video_data = json.load(file)
            data_list.append({
                "channelId": video_data.get("channelId"),
                "channelTitle": video_data.get("channelTitle"),
                "title": video_data.get("title"),
                "description": video_data.get("description"),
                "tags": video_data.get("tags", []),
                "categoryId": video_data.get("categoryId"),
                "topicCategories": video_data.get("topicCategories", []),
                "thumbnail_url": video_data.get("thumbnails", {}).get("standard", {}).get("url")
            })

data = pd.DataFrame(data_list)
data.to_pickle('./Data/raw_data.pkl')  

data = pd.read_pickle("./Data/raw_data.pkl")
print(data.columns)