from fastapi import FastAPI
import uvicorn
from database import Database
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
db = Database()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    positions = db.select(query="SELECT * FROM positions")
    return positions

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info",reload=True)