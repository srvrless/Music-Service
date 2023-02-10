FROM python:3.10-slim

WORKDIR /usr/src/application

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .


CMD ["uvicorn", "src.core.app:app", "--host", "0.0.0.0", "--port", "8000"]