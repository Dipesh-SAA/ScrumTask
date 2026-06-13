# Calculator API

FastAPI backend for calculator operations.

## Run locally

bash
pip install -r requirements.txt
uvicorn main:app --reload


## Run with Docker

bash
docker build -t calculator-api .
docker run -p 80:80 calculator-api
