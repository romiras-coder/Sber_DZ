import datetime
import numpy as np
import uvicorn
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime, time, timedelta

app = FastAPI()


class Item(BaseModel):
    date: str
    periods: int
    amount: int
    rate: float

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
                "periods": 7,
                "amount": 10000,
                "rate": 8,
            }
        }


@app.get("/")
async def root():
    return {"message": "Hello World"}


# создание нового пользователя, метод POST, поля формы, возврат JSON
@app.post("/test/")
async def create_item(item: Item):
    # item_dict = item.dict()
    # print(item_dict)
    # print(item_dict['date'], type(item_dict['date']))
    # print(item_dict['periods'], type(item_dict['periods']))
    # print(item_dict['amount'], type(item_dict['amount']))
    # print(item_dict['rate'], type(item_dict['rate']))

    # if item_dict['periods'] not in range(1, 60):
    #     raise HTTPException(status_code=400, detail={"error": f"период не может быть отрицательным"})
    # elif item_dict['periods'] > 60:
    #     raise HTTPException(status_code=400, detail={"error": f"период не может быть больше 60 месяцев"})
    # elif item_dict['amount'] > 60:
    #     raise HTTPException(status_code=400, detail={"error": f"период не может быть больше 60 месяцев"})

    # if item_dict.:
    #     raise HTTPException(
    #         status_code=400, detail=f"Username '{user.username}' already registered")

    # if item.tax:
    #     price_with_tax = item.price + item.tax
    #     item_dict.update({"price_with_tax": price_with_tax})
    return item


# main
if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
