FROM python:3.11-slim

RUN apt update && apt install -y ffmpeg espeak libespeak1 fonts-dejavu-core && apt clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]