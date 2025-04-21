FROM python:alpine

WORKDIR /app

COPY requirements.txt /app/

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
