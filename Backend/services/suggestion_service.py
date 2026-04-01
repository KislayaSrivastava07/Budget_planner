import pandas as pd


def generate_suggestions(transactions, budgets):

    suggestions = []

    df = pd.DataFrame([{
        "amount": t.amount,
        "category": t.category,
        "type": t.type
    } for t in transactions])

    if df.empty:
        return ["No spending data available"]

    expenses = df[df["type"] == "expense"]

    category_spending = expenses.groupby("category")["amount"].sum()

    for budget in budgets:

        spent = category_spending.get(budget.category, 0)

        if spent > budget.monthly_limit:
            diff = spent - budget.monthly_limit
            suggestions.append(
                f"You exceeded {budget.category} budget by ₹{diff}"
            )

    if not suggestions:
        suggestions.append("Your spending is within the budget!")

    return suggestions