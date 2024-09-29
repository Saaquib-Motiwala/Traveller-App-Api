from fastapi import FastAPI
from helpers import get_states_list, get_state_data, get_attr_details

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/states/")
async def states():
    states_list = get_states_list()
    return {"data": states_list}

@app.get("/states/{state_id}")
async def states(state_id: int):
    state_data = get_state_data(state_id)
    return {"data": state_data}

@app.get("/attractions/{attr_id}")
async def attractions(attr_id: int):
    attr_details = get_attr_details(attr_id)
    return {"data": attr_details}



