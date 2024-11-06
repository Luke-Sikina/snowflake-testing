FROM python:3.9.20

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./requests/* .

CMD ["python", "ALS-7642.py"]