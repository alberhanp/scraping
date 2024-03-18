from fastapi import FastAPI, Request
from routes import routers
import uvicorn

app = FastAPI()

app.include_router(routers.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)

