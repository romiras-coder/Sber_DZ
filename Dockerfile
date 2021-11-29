FROM python:3.9.5
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD [ "python", "./main.py" ]