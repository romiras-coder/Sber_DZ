import datetime

import uvicorn
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time, timedelta

app = FastAPI()


class Item(BaseModel):
    date: str
    periods: int
    amount: int
    rate: float

    class Config:
        schema_extra = {
            "example": {
                "date": "31.01.2021",
                "periods": 7,
                "amount": 10000,
                "rate": 8.1,
            }
        }


@app.get("/")
async def root():
    return {"message": "Hello World"}


# создание нового пользователя, метод POST, поля формы, возврат JSON
@app.post("/test/")
async def create_item(item: Item):
    item_dict = item.dict()
    print(item_dict)
    print(item_dict['date'], type(item_dict['date']))
    print(item_dict['periods'], type(item_dict['periods']))
    print(item_dict['amount'], type(item_dict['amount']))
    print(item_dict['rate'], type(item_dict['rate']))

    if item_dict['periods'] not in range(1, 60):
        raise HTTPException(status_code=400, detail={"error": f"период не может быть отрицательным"})
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
    return item_dict


# main
if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
