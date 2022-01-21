# syntax=docker/dockerfile:1
FROM python:3.8.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /dict
COPY requirements.txt /dict/
RUN pip install -r requirements.txt
COPY . /dict/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]