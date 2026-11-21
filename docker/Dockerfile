FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv/server-2
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium chromium-driver fonts-liberation libnss3 libatk-bridge2.0-0 \
    libgtk-3-0 libgbm1 libasound2 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
