from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator

APP = FastAPI()


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@APP.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=400,
        content={"error": f"{exc.name}"},
    )


class Item(BaseModel):
    date: str
    periods: int
    amount: int
    rate: float

    class Config:
        schema_extra = {
            "example": {
                "date": "31.01.2021",
                "periods": 3,
                "amount": 10000,
                "rate": 6,
            }
        }

    @validator('date')
    def date_must_be_str(cls, date: str):
        '''
        :param date:
        :return: date or Exception
        '''
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return date
        except:
            raise UnicornException(name="дата (date) должен быть строкой формата дд.мм.гггг")

    @validator('periods')
    def periods_in_interval(cls, periods: int):
        '''
        :param periods:
        :return: periods or Exception
        '''
        if periods not in range(1, 61):
            raise UnicornException(name="период (periods) должен быть не меньше 1 и не больше 60")
        return periods

    @validator('amount')
    def amount_must_be_in_interval(cls, amount: int):
        '''
        :param amount:
        :return: amount or Exception
        '''
        if amount not in range(10000, 3000001):
            raise UnicornException(name="сумма вклада (amount) должна быть не меньше 10000 и не превышать 3000000")
        return amount

    @validator('rate')
    def rate_must_be_in_interval(cls, rate: float):
        '''
        :param rate:
        :return: rate or Exception
        '''
        if rate not in np.arange(1.0, 8.1, 0.1).round(1):
            raise UnicornException(name="процентная ставка (rate) должна быть не меньше 1 и не превышать 8")
        return rate


@APP.get("/test/")
async def test():
    '''
    :return: message
    '''
    return {"message": "OK"}


@APP.post("/")
async def root(item: Item):
    '''
    :param item:
    :return: JSONResponse
    '''
    count = 0
    summa = item.amount
    data = {}
    for _ in range(item.periods):
        summa += round(summa * (1 + item.rate / 12 / 100) - summa, 2)
        data[(datetime.strptime(item.date, "%d.%m.%Y") + relativedelta(months=count)).strftime('%d.%m.%Y')] = round(
            summa, 2)
        count += 1

    return JSONResponse(content=data)


if __name__ == '__main__':
    uvicorn.run('main:APP', host='0.0.0.0', port=8000)
