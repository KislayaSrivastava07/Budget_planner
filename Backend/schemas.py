from pydantic import BaseModel
from datetime import date


class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    description: str
    date: date


class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_orm = True


class BudgetCreate(BaseModel):
    category: str
    monthly_limit: float
    month: str


class BudgetResponse(BudgetCreate):
    id: int

    class Config:
        form_mode = True