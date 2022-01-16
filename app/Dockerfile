# FROM python:3.8-slim-buster
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# COPY . .
# ENV FLASK_APP=app
# EXPOSE 5000
# EXPOSE 9090
# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD [ "flask", "run"]

# FROM python:3
# WORKDIR /app
# ADD . /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# COPY . .
# ENV FLASK_APP=app
# EXPOSE 5000
# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["python", "app.py", "--host=0.0.0.0"]

# FROM python:3
# RUN mkdir /code
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# EXPOSE 5000
# COPY . /code/
# CMD ["flask", "run"]

FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ENV FLASK_APP=app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code/
CMD [ "flask", "run", "--host=0.0.0.0"]