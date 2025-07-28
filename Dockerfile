FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install pymupdf

CMD ["python", "extractor.py"]

