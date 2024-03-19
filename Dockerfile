FROM python:3.12
WORKDIR /app
COPY . /app
COPY token /app/token
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "dnd_telegram_bot"]
