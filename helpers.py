import pandas as pd
from ast import literal_eval
import json
import re
import g4f



class DataRetriever:
    def __init__(self):
        self.state_df = pd.read_csv("states_info.csv")
        self.attr_df = pd.read_csv("attraction_details.csv")
        self.sys_prompt = """You are an expert travel itinerary planner. Create a detailed day-wise itinerary for a trip to a specific destination. Ensure the itinerary follows a particular theme and includes relevant activities.

Instructions:
Trip Details:

Number of Days: [NUMBER OF DAYS]
Destination: [DESTINATION]
Theme: [TYPE OF VACATION] (e.g., adventure, cultural, relaxation)
Activity Suggestions:

List relevant activities (e.g., hiking, historical tours, beach lounging).
Daily Format:
Return the itinerary as a Python list of dictionaries. Each dictionary should represent a day and include:

"day": The day number (e.g., "Day 1").
"description": A detailed summary of the day's activities."""
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

    def get_recommended_attr(self, rec_ids):
        attr_id_list = []
        for rec_id in rec_ids:
            attr_id_list.extend(self.tags_dict[self.category_map[rec_id]])

        recomm_attr = self.attr_df.loc[self.attr_df['id'].isin(attr_id_list)]
        recomm_attr = recomm_attr.sort_values(by="review_count", ascending=False)
        recomm_attr = recomm_attr.head(10)
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

    async def get_ai_itinerary(self, prompt: str):
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
                messages=[{"role": "system", "content": self.sys_prompt}, {"role": "user", "content": f"{prompt}"}],
        )

        response_match = re.search(r'\[(.*\n)*\]', response)
        return eval(response_match.group(0))


if __name__ == "__main__":
    dr = DataRetriever()
    # print(dr.get_search_result("Maha   ", "all"))
    # print(dr.get_liked_attr([1491020, 2704519, 317329, 319875, 321437]))
    # print(dr.get_category_attr(1))
    # print(dr.get_recommended_attr([0,1]))
    # print(dr.get_ai_resp("Manali for 2 days and leisure trip"))
    pass
