FROM python:3.13.3-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "web.py"]