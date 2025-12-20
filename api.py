from fastapi import FastAPI

app = FastAPI()

iot_data = {
    1: {
        "name": "esp32",
        "temp": 14
    }
}

@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/data")
def get_data(name: str):
    for id in iot_data:
        if iot_data[id]["name"] == name:
            return iot_data[id]
    return "No data found, maybe add some data"