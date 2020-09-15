FROM python:3.8.5

RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD gunicorn foodgram_project.wsgi:application --bind 0.0.0.0:8000