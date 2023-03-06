FROM python:3.10.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/api

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.core.app:app", "--host", "0.0.0.0", "--port", "8000"]