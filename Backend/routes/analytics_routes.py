from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import crud
from services.suggestion_service import generate_suggestions

router = APIRouter()


@router.get("/spending-insights")
def spending_insights(db: Session = Depends(get_db)):

    transactions = crud.get_transactions(db)
    budgets = crud.get_budgets(db)

    suggestions = generate_suggestions(transactions, budgets)

    return {"suggestions": suggestions}