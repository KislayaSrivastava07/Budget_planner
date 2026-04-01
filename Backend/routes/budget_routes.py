from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter()


@router.post("/set-budget")
def set_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    return crud.create_budget(db, budget)


@router.get("/budgets")
def get_budgets(db: Session = Depends(get_db)):
    return crud.get_budgets(db)