from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from calculator import calculate
from datetime import datetime
from json import dump, load

history = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global history

    try:
        with open("history.json", "r") as file:
            history = load(file)
    except FileNotFoundError:
        pass

    yield

    with open("history.json", "w") as file:
        dump(history, file)


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:63342",  # Local development environment
    # Add any other origins you need to allow here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/calculate/")
async def read_item(expression: str, user: str):
    expression = expression.replace(" ", "")

    try:
        result = calculate(expression)
    except Exception as e:
        return {"result": str(e)}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(
        {
            "user_id": user,
            "expression": expression,
            "result": result,
            "timestamp": timestamp,
        }
    )

    return {"result": result}


@app.get("/history/{user}")
async def read_item(user: str):
    if user == "all":
        return history

    return [entry for entry in history if entry["user_id"] == user]
