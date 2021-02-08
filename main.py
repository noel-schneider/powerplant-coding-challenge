from fastapi import FastAPI
from power_planer import compute_optimal_loads

app = FastAPI()


@app.post("/productionplant")
async def read_item(payload: dict):
    return compute_optimal_loads(payload)
