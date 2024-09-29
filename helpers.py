import pandas as pd
from ast import literal_eval
import json
import requests

def get_states_list():
    states_list = pd.read_csv("states_id.csv").to_dict(orient="split")
    return states_list["data"]


def get_state_data(state_id):
    attr_df = pd.read_csv("attraction_details_2.csv")
    attr_filtered = attr_df[attr_df["state_id"] == state_id]
    attr_filtered = attr_filtered[["id", "name", "images"]]
    attr_filtered["images"] = attr_filtered["images"].apply(lambda x: literal_eval(x))
    attr_filtered["images"] = attr_filtered["images"].apply(lambda x: x[0])
    attr_filtered_dict = attr_filtered.to_dict(orient="records")
    return attr_filtered_dict

def get_attr_details(attr_id):
    attr_df = pd.read_csv("attraction_details_2.csv")
    attr = attr_df.loc[attr_df["id"] == attr_id]
    attr.loc[:, "images"] = attr["images"].apply(lambda x: literal_eval(x))
    attr.loc[:, "tags"] = attr["tags"].apply(lambda x: literal_eval(x))
    attr.loc[:, "reviews"] = attr["reviews"].apply(lambda x: literal_eval(x))
    attr_dict = attr.to_dict(orient="records")[0]
    # attr_dict = json.loads(attr_dict)
    weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={attr_dict['lat']}&longitude={attr_dict['long']}&current=")
    print(weather.content)
    return attr_dict["lat"]


if __name__ == "__main__":
    print(get_attr_details(1220147))