FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev postgresql-client bash libffi-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
