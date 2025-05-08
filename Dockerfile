FROM python/3.13.3-slim

WORKDIR /whitemanta

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "web.py"]
