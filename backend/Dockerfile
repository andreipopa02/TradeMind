FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm -rf /app/mt5_service

EXPOSE 8000

CMD ["sh", "-c", "python3 init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]


