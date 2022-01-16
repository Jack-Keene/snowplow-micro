FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ENV FLASK_APP=app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code/
CMD [ "flask", "run", "--host=0.0.0.0"]