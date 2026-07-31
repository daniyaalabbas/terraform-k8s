FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
