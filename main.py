from fastapi import FastAPI
from helpers import DataRetriever

app = FastAPI()
dr = DataRetriever()

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


@app.get("/recommended_attr/")
async def states():
    recomm_dict = dr.get_recommended_attr()
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




