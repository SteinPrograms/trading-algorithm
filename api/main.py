from fastapi import FastAPI
import psycopg2
import psycopg2.extras
from logs import logger
import os
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getPositionsData")
async def read__positions_table():
    return Database().get_positions_data()


@app.get("/getServerData")
async def read___table():
    return Database().get_server_data()

class Database:
    """Database SDK"""

    def select(
            self,
            *,
            query: str,
        ):
        """Select data from the database"""
        try:
            with psycopg2.connect(
                host=os.getenv('POSTGRES_HOST'),
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                ) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall().copy()
            return result
        except psycopg2.OperationalError as error:
            logger.error("Database error : %s",error)

    def get_server_data(
        self):
        """Get server data from database"""

        return self.select(
            query = "SELECT * FROM server"
        )
    
    def get_positions_data(
        self):
        """Get server data from database"""

        return self.select(
            query = "SELECT * FROM positions"
        )

if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8080,reload=True,root_path="/")