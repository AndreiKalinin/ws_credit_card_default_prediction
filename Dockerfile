FROM python:3.10-slim

WORKDIR /root/application

COPY ./application/app.py ./root/application/app.py

RUN pip install flask gunicorn numpy pandas scikit-learn flask_wtf python-dotenv