FROM python:3.11-slim

WORKDIR /app

COPY services/paper_broker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/paper_broker/app ./app
COPY contracts ./contracts

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
