from starlette.testclient import TestClient
from .main import APP

Client = TestClient(APP)


def test_get_test():
    '''  проверяем статус сервера на тестовой страничке  - пустой GET-запрос '''
    response = Client.get("/test/")
    assert response.status_code == 200
    assert response.json() == {'message': 'OK'}


def test_post_test():
    '''  проверяем статус сервера на тестовой страничке  - пустой POST-запрос '''
    response = Client.post("/test/")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}


def test_good_post_root():
    '''  проверяем статус сервера на главной страничке  - POST-запрос с корректными данными '''
    response = Client.post("/", json={
        "date": "31.01.2021",
        "periods": 12,
        "amount": 10000,
        "rate": 8
    })
    assert response.status_code == 200
    assert response.json() == {
        "31.01.2021": 10066.67,
        "28.02.2021": 10133.78,
        "31.03.2021": 10201.34,
        "30.04.2021": 10269.35,
        "31.05.2021": 10337.81,
        "30.06.2021": 10406.73,
        "31.07.2021": 10476.11,
        "31.08.2021": 10545.95,
        "30.09.2021": 10616.26,
        "31.10.2021": 10687.04,
        "30.11.2021": 10758.29,
        "31.12.2021": 10830.01
    }


def test_bad_date_post_root():
    '''  проверяем статус сервера на главной страничке  - POST-запрос с НЕ корректными данными даты '''
    response = Client.post("/", json={
        "date": "31.01.2021111",
        "periods": 12,
        "amount": 10000,
        "rate": 8
    })
    assert response.status_code == 400
    assert response.json() == {"error": "дата (date) должен быть строкой формата дд.мм.гггг"}


def test_bad_period_post_root():
    '''  проверяем статус сервера на главной страничке  - POST-запрос с НЕ корректными данными периода '''
    response = Client.post("/", json={
        "date": "31.01.2021",
        "periods": 122,
        "amount": 10000,
        "rate": 8
    })
    assert response.status_code == 400
    assert response.json() == {"error": "период (periods) должен быть не меньше 1 и не больше 60"}


def test_bad_amount_post_root():
    '''  проверяем статус сервера на главной страничке  - POST-запрос с НЕ корректными данными периода '''
    response = Client.post("/", json={
        "date": "31.01.2021",
        "periods": 12,
        "amount": 10,
        "rate": 8
    })
    assert response.status_code == 400
    assert response.json() == {
        "error": "сумма вклада (amount) должна быть не меньше 10000 и не превышать 3000000"
    }


def test_bad_rate_post_root():
    '''  проверяем статус сервера на главной страничке  - POST-запрос с НЕ корректными данными процентной ставки '''
    response = Client.post("/", json={
        "date": "31.01.2021",
        "periods": 12,
        "amount": 10000,
        "rate": 10
    })
    assert response.status_code == 400
    assert response.json() == {
        "error": "процентная ставка (rate) должна быть не меньше 1 и не превышать 8"
    }
