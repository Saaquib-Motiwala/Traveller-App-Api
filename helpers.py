import pandas as pd
from ast import literal_eval
import json
import requests


class DataRetriever:
    def __init__(self):
        self.state_df = pd.read_csv("states_info.csv")
        self.attr_df = pd.read_csv("attraction_details.csv")
        self.category_map = [
            "Hiking Trails",
            "Religious Sites",
            "Beaches",
            "Mountains",
            "Historic Sites",
            "Natural History Museums",
            "National Parks",
            "Nature & Wildlife Areas"
        ]
        with open("tags.json", "r") as file:
            self.tags_dict = json.load(file)

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
        attr_filtered = attr_filtered[["id", "name", "cover_img", "city_name"]]
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

    def get_search_result(self, query: str, type):
        query = query.rstrip()
        if type == "all":
            state_search_res = self.state_df[self.state_df["STATE_NAME"].str.contains(query, case=False)]
            if not state_search_res.empty:
                state_search_res.loc[:, "type"] = "state"
            state_search_res = state_search_res.to_dict(orient="records")

            attr_search_res = self.attr_df[self.attr_df["name"].str.contains(query, case=False)]
            if not attr_search_res.empty:
                attr_search_res.loc[:, "type"] = "attraction"
            attr_search_res = attr_search_res.to_dict(orient="records")
            search_res = state_search_res + attr_search_res

        elif type == "state":
            search_res = self.state_df[self.state_df["STATE_NAME"].str.contains(query, case=False)]
            if not search_res.empty:
                search_res.loc[:, "type"] = "state"
            search_res = search_res.to_dict(orient="records")
        else:
            search_res = self.attr_df[self.attr_df["name"].str.contains(query, case=False)]
            if not search_res.empty:
                search_res.loc[:, "type"] = "attraction"
            search_res = search_res.to_dict(orient="records")

        return search_res

    def get_liked_attr(self, liked_ids: list):
        liked_attr = self.attr_df.loc[self.attr_df['id'].isin(liked_ids)]
        liked_attr = liked_attr.loc[:, ["id", "name", "city_name", "state_name", 'cover_img']]
        liked_dict = liked_attr.to_dict(orient="records")
        return liked_dict

    def get_category_attr(self, category_id: int):

        attr_id_list = self.tags_dict[self.category_map[category_id]]
        filtered_attr = self.attr_df.loc[self.attr_df["id"].isin(attr_id_list)]
        filtered_attr = filtered_attr.sort_values("review_count", ascending=False)
        filtered_attr = filtered_attr.loc[:, ["id", "name", "city_name", "state_name", 'cover_img']]
        filtered_dict = filtered_attr.to_dict(orient="records")
        return filtered_dict


if __name__ == "__main__":
    # dr = DataRetriever()
    # print(dr.get_search_result("Maha   ", "all"))
    # print(dr.get_liked_attr([1491020, 2704519, 317329, 319875, 321437]))
    # print(dr.get_category_attr(1))
    pass
