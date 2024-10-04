import pandas as pd
from ast import literal_eval
import json
import requests


class DataRetriever:
    def __init__(self):
        self.state_df = pd.read_csv("states_info.csv")
        self.attr_df = pd.read_csv("attraction_details.csv")

    def get_states_list(self):
        states_list = self.state_df.to_dict(orient="split")
        states_list = [[i[0], i[1], i[4]] for i in states_list["data"]]
        return states_list

    def get_state_data(self, state_id):
        filtered_state = self.state_df.loc[self.state_df["STATE_ID"] == state_id]
        state_name = filtered_state["STATE_NAME"].values[0]
        state_capital = filtered_state["STATE_CAPITAL"].values[0]
        state_info = filtered_state["STATE_INFO"].values[0]
        state_image = filtered_state["STATE_IMAGE"].values[0]
        attr_filtered = self.attr_df[self.attr_df["state_id"] == state_id]
        attr_filtered = attr_filtered[["id", "name", "cover_img"]]
        attr_filtered_dict = attr_filtered.to_dict(orient="records")
        return {"state_data": {"state_name": state_name, "state_capital": state_capital, "state_info": state_info, "state_image": state_image}, "attr_data": attr_filtered_dict}

    def get_attr_details(self, attr_id):
        attr = self.attr_df.loc[self.attr_df["id"] == attr_id]
        attr.loc[:, "images"] = attr["images"].apply(lambda x: literal_eval(x))
        attr.loc[:, "tags"] = attr["tags"].apply(lambda x: literal_eval(x))
        attr.loc[:, "reviews"] = attr["reviews"].apply(lambda x: literal_eval(x))
        attr_dict = attr.to_dict(orient="records")[0]
        return attr_dict

    def get_recommended_attr(self):
        lst = [317329, 319875, 311667, 319695, 2704519, 12687575, 320061, 321437, 2697362, 1491020]
        recomm_attr = self.attr_df.loc[self.attr_df['id'].isin(lst)]
        recomm_dict = recomm_attr.to_dict(orient="records")
        return recomm_dict

    def get_search_result(self, query):
        search_res = self.attr_df[self.attr_df["name"].str.contains(query, case=False)].to_dict(orient="records")
        return search_res



if __name__ == "__main__":
    # print(get_attr_details(25555680)["reviews"])
    # print(get_recommended_attr())
    dr = DataRetriever()
    print(dr.get_search_result("Taj"))
