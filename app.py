from fastapi import FastAPI
import uvicorn
from src.controller import message_adapter

app = FastAPI()
app.include_router(message_adapter.adapter)


@app.get('/')
async def root():
    return "Hello world!"


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
