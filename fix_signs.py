from finance import DB, OperationType

def fix_logic(t):
    # Если Трата/Долг, но число положительное -> делаем минус
    if t.op_type in [OperationType.SPEND, OperationType.LENT] and t.amount > 0:
        t.amount = -t.amount
    # Если Приход/Возврат, но число отрицательное -> делаем плюс
    elif t.op_type in [OperationType.INCOME, OperationType.RETURNED] and t.amount < 0:
        t.amount = abs(t.amount)

db = DB()
db.each(fix_logic) # Проходим по всем записям
db.commit()        # Сохраняем