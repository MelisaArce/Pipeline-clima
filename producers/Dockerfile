FROM python:3.9

WORKDIR /app

COPY producer.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python producer.py && tail -f /dev/null"]

