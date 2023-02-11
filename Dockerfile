FROM python:3.10-alpine

WORKDIR /usr/src/api

COPY requirements.txt ./

RUN  pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["uvicorn", "src.core.app:app", "--host", "0.0.0.0", "--port", "8000"]