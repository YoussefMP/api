FROM python:3.13-slim

WORKDIR /App

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["fastapi", "run", "./API_App/main.py", "--host", "0.0.0.0", "--port", "8080"]