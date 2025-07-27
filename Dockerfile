FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY app/ /app

RUN pip install --no-cache-dir -r requirement.txt

CMD ["python", "1a.py"]
