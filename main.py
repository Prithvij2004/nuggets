from api.main import api_router

from fastapi import FastAPI

from core.db.main import create_db_and_tables

app = FastAPI()
app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    print("creating Database")
    create_db_and_tables()
    print("Database created")


