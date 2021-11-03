"Main app"


import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    # For debugging
    uvicorn.run(app, host="localhost", port=8000)
