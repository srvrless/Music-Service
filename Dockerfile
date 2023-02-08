FROM python:3.10-alpine

WORKDIR /usr/src/application

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["uvicorn", "src.core.run:app", "--host", "0.0.0.0", "--port", "8000"]