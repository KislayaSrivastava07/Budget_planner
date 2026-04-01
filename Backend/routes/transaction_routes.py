from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter()


@router.post("/add-transaction")
def add_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)


@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)


@router.delete("/transaction/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return crud.delete_transaction(db, transaction_id)