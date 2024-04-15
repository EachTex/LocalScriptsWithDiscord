import json, requests, random, datetime, math
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

app = FastAPI()

class ConnectData(BaseModel):
    products: list
    auth_pin: int

class ConnectDetails(BaseModel):
    auth_pin: int
    connect_id: int

@app.get("/")
async def get_localconnect():
    return JSONResponse(
        content = {
            "status": 403,
            "details": "forbidden"
        },
        status_code = 403
    )

@app.post("/")
async def local_connect(data: ConnectData):
    with open(f"./localnet.json", "r") as f:
        connect = json.load(f)
        f.close()

    connect_id = random.randint(10000, 99999)
    while connect_id in connect.keys():
        connect_id = random.randint(10000, 99999)

    expired_stamp = math.floor(datetime.datetime.now().timestamp()) + 1800

    connect[str(connect_id)] = {
        "products": data.products,
        "auth_pin": data.auth_pin,
        "expire_at": expired_stamp,
        "status": {
            "code": 0, # 0: Waiting for connect, 1: Connected 2: Changed (waiting for responses)
            "owner": 0
        }
    }

    with open(f"./localnet.json", "w") as f:
        json.dump(connect, f, indent = 4, ensure_ascii = False)
        f.close()

    return JSONResponse(content = {
        "status": "successful",
        "connect_id": connect_id
    }, status_code = 200)

@app.post("/status")
async def status_connect(data: ConnectDetails):
    with open(f"./localnet.json", "r") as f:
        connect = json.load(f)
        f.close()

    try:
        _status_code = connect[str(data.connect_id)]['status']['code']
        if _status_code == 0:
            return JSONResponse(
                content = {
                    "status": 0
                },
                status_code = 200
            )
        elif _status_code == 1:
            return JSONResponse(
                content = {
                    "status": 1,
                    "user_id": connect[str(data.connect_id)]['status']['owner']
                }
            )
        else:
            return JSONResponse(
                content = {
                    "status": _status_code,
                    "products": connect[str(data.connect_id)]['products']
                },
                status_code = 200
            )

    except:
        return JSONResponse(
            content = {
                "status": 404,
                "details": "Data not found."
            },
            status_code = 404
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=12958)