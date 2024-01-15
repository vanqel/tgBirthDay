import uvicorn
from fastapi import FastAPI
import asyncio

import engine

app = FastAPI()


@app.post("/sendjsonforms")
async def getjson(json):
    with open('storage/StorageBirthsDay.json', 'w') as json_file:
        await json.dump(json, json_file)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")