# Tutorial.org - Snowplow Micro Demonstration
Tutorial.org is a web app written in Python using the Flask framework. It includes user tracking through Snowplow Micro using the Python tracker to track a number of user events including:

* Login events 
* Page views  
* Donation events
* Feedback events (eg Like & Dislike)

It uses context for some of these events including:
* User information
* Article information

## Running the application

To launch the docker container run the below:
```html

Build Image
docker-compose build

Run Micro
docker-compose up -d

Launch Flask App
python app/app.py

```
  
The collector endpoint will be http://localhost:9090.

To view the collected events use the endpoints:

* `/micro/all`: summary
* `/micro/good`: good events
* `/micro/bad`: bad events
* `/micro/reset`: clears cache

The Flask homepage will be on http://127.0.0.1:5000/
