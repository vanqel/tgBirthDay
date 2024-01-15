from fastapi import FastAPI

app = FastAPI()


@app.post("/sendjsonforms")
async def getjson(json):
    with open('storage/StorageBirthsDay.json', 'w') as json_file:
        await json.dump(json, json_file)
