FROM ubuntu:latest
WORKDIR /app

RUN apt update && apt install -y python3 python3-pip

COPY requirements.txt .

RUN pip3 install --break-system-packages -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
