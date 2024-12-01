from fastapi import FastAPI
from pydantic import BaseModel
from helpers import DataRetriever

app = FastAPI()
dr = DataRetriever()


class LikedList(BaseModel):
    likedlist: list


class RecommendedList(BaseModel):
    recommListId: list


class Ai(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/states/")
async def states():
    states_list = dr.get_states_list()
    return {"data": states_list}


@app.post("/recommended_attr/")
async def states(recs: RecommendedList):
    recomm_dict = dr.get_recommended_attr(recs.recommListId)
    return {"data": recomm_dict}


@app.get("/search/query={query}&type={type}")
async def search(query: str, type: str):
    search_res = dr.get_search_result(query, type)
    return {"data": search_res}


@app.get("/states/{state_id}")
async def states(state_id: int):
    state_data = dr.get_state_data(state_id)
    return {"data": state_data}


@app.get("/attractions/{attr_id}")
async def attractions(attr_id: int):
    attr_details = dr.get_attr_details(attr_id)
    return {"data": attr_details}

@app.get("/category/{category_id}")
async def attractions(category_id: int):
    attr_details = dr.get_category_attr(category_id)
    return {"data": attr_details}

@app.post("/liked")
async def liked(liked: LikedList):
    liked_attr = dr.get_liked_attr(liked.likedlist)
    return {"data": liked_attr}

@app.post("/itinerary")
async def ai(ai: Ai):
    itinerary = dr.get_ai_itinerary(ai.prompt)
    return {"data": itinerary}
