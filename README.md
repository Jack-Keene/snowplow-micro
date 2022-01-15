# Tutorials.org - Snowplow Micro Demonstration
Tutorial.org is a web app written in Python using the Flask framework. It includes user tracking through Snowplow Micro using the Python tracker. 

## Running the application

To launch the docker container run the below:
```cmd

docker run 
  --mount type=bind,source=$(pwd)/micro,destination=/config \
  -p 9090:9090 \
  snowplow/snowplow-micro:latest \
  --collector-config /config/micro.conf \
  --iglu /config/iglu.jsonfig/iglu.json
  
  ```
  
The collector endpoint will be http://localhost:9090.

To view the collected events use the endpoints:

* /micro/all: summary
* /micro/good: good events
* /micro/bad: bad events
* /micro/reset: clears cache


To run the flask application:
``` cmd

Bash

$ export FLASK_APP=hello
$ flask run
 
CMD
 
set FLASK_APP=hello
flask run

Powershell

$env:FLASK_APP = "hello"
flask run

```

This will launch the homepage on http://127.0.0.1:5000/
