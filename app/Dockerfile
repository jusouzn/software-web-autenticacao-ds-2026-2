FROM python:3.12-slim

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . app/

RUN useradd --no-create-home aplicacao
USER aplicacao

EXPOSE 8000
CMD ["uvicorn", "app.principal:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
