import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = FastAPI()


class Item(BaseModel):
    date: str
    periods: int
    amount: int
    rate: float

    @validator('date')
    def date_must_be_str(cls, v):
        try:
            datetime.strptime(v, "%d.%m.%Y")
            return v
        except:
            raise HTTPException(status_code=400,
                                detail={"error": f"дата (date) должен быть строкой формата дд.мм.гггг"})

    @validator('periods')
    def periods_must_be_in_interval(cls, v):
        if v not in range(1, 61):
            raise HTTPException(status_code=400,
                                detail={"error": f"период (periods) должен быть не меньше 1 и не больше 60"})
        return v

    @validator('amount')
    def amount_must_be_in_interval(cls, v):
        if v not in range(10000, 3000001):
            raise HTTPException(status_code=400,
                                detail={
                                    "error": f"сумма вклада (amount) должна быть не меньше 10000 и не превышать 3000000"})
        return v

    @validator('rate')
    def rate_must_be_in_interval(cls, v):
        if v not in np.arange(1.0, 8.1, 0.1).round(1):
            raise HTTPException(status_code=400,
                                detail={"error": f"процентная ставка (rate) должна быть не меньше 1 и не превышать 8"})
        return v

    class Config:
        schema_extra = {
            "example": {
                "date": "31.01.2021",
                "periods": 3,
                "amount": 10000,
                "rate": 6,
            }
        }


@app.get("/test/")
async def test():
    return {"message": "Hello World"}


@app.post("/")
async def root(item: Item):
    count = 0
    summa = item.amount
    data = {}
    for i in range(item.periods):
        summa += round(summa * (1 + item.rate / 12 / 100) - summa, 2)
        data[(datetime.strptime(item.date, "%d.%m.%Y") + relativedelta(months=count)).strftime('%d.%m.%Y')] = round(
            summa, 2)
        count += 1
    print(data)

    return JSONResponse(content=data)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
