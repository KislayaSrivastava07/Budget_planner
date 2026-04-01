from fastapi import FastAPI

from database import engine
import models

from routes import transaction_routes
from routes import budget_routes
from routes import analytics_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personalized Money Tracker")

app.include_router(transaction_routes.router)
app.include_router(budget_routes.router)
app.include_router(analytics_routes.router)


@app.get("/")
def root():
    return {"message": "Money Tracker API Running"}