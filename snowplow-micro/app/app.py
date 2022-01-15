from flask import Flask, render_template, request, session, flash
from werkzeug.utils import redirect
from functools import wraps
import time
import json

from snowplow_tracker import Tracker, Emitter, SelfDescribingJson

app = Flask(__name__)
app.secret_key="secret_key"

host = "http://localhost:5000"

e = Emitter("127.0.0.1:9090")
tracker = Tracker(e)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" not in session.keys():
            return redirect('/login')
        return f(*args, **kwargs)
    return wrap

@app.route('/login', methods=["GET", "POST"])
def login():
    # Track User Visit
    tracker.track_page_view(host + "/login", referrer = request.referrer)

    if request.method == "POST":
        session['logged_in'] = True
        session['username'] = request.form['username']
        session['start_time'] = time.time() * 1000

        
        flash('You have successfully logged in', 'success')
        
        #Track User Login   
        user_context = SelfDescribingJson(
            "iglu:com.snowplowanalytics/user_entity/jsonschema/1-0-0",
            {
                "username": session['username']
            }) 

        tracker.track_self_describing_event(SelfDescribingJson(
            "iglu:com.snowplowanalytics/login_event/jsonschema/1-0-0",
            {
                "login_event": "login"
            }
        ), 
            context=[user_context])
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Track User Logout
    session_length = time.time()*1000 - session['start_time']

    user_context = SelfDescribingJson("iglu:com.snowplowanalytics/user_entity/jsonschema/1-0-0",
        {
            "username": session['username'],
            "session_length": session_length
        }) 

    tracker.track_self_describing_event(SelfDescribingJson(
        "iglu:com.snowplowanalytics/login_event/jsonschema/1-0-0",
        {
            "login_event": "logout"
        }
    ),
        context=[user_context])
    session.clear()
    flash('You have successfully logged out', 'success')        

    return redirect('/')

@app.route('/')
@login_required
def index():
    user_context = SelfDescribingJson(
        "iglu:com.snowplowanalytics/user_entity/jsonschema/1-0-0",
        {
            "username": session['username']
        }
    ) 

    tracker.track_page_view(host, context=[user_context], referrer = request.referrer)
    return render_template("index.html", user=session['username'])

@app.route('/articles')
@login_required
def articles():
    with open("../snowplow-micro/app/assets/blogs.json") as file:
        blogs = json.load(file)

    user_context = SelfDescribingJson(
        "iglu:com.snowplowanalytics/user_entity/jsonschema/1-0-0",
        {
            "username": session['username']
        }
    ) 

    tracker.track_page_view("http://localhost:5000/articles", context=[user_context] , referrer = request.referrer)
    return render_template("articles.html", blogs=blogs)

@app.route('/article/<string:id>', methods= ["GET", "POST"])
def article(id):
    with open("../snowplow-micro/app/assets/blogs.json") as file:
        blogs = json.load(file)

    user_context = SelfDescribingJson(
        "iglu:com.snowplowanalytics/user_entity/jsonschema/1-0-0",
        {
            "username": session['username']
        }
    ) 

    for blog in blogs:
        if blog['_id'] == id:
            article_context = SelfDescribingJson(
                "iglu:com.snowplowanalytics/article_entity/jsonschema/1-0-0",
                {
                    "id": blog['_id'],
                    "title": blog['title'],
                    "published": blog['published']
                }
            )

            tracker.track_page_view("http://localhost:5000/article/" + id, context=[article_context, user_context], referrer = request.referrer)

            #track user likes and dislikes
            if request.method == "POST":
                tracker.track_self_describing_event(SelfDescribingJson(
                    "iglu:com.snowplowanalytics/feedback_event/jsonschema/1-0-0",
                    {
                        "feedback_event": request.form['_feedback']
                    }
                ), 
                    context=[user_context, article_context])

            return render_template('article.html', blog=blog)

@app.route('/donate', methods=["GET", "POST"])
@login_required
def donate():

    user_context = SelfDescribingJson(
        "iglu:com.snowplowanalytics/user_entity/jsonschema/1-0-0",
        {
            "username": session['username']
        }
    ) 

    tracker.track_page_view(host + "/donate", context=[user_context], referrer=request.referrer)

    if request.method == "POST":
        tracker.track_self_describing_event(SelfDescribingJson(
            "iglu:com.snowplowanalytics/donate_event/jsonschema/1-0-0",
            {
                "donation": int(request.form['donation'])
            }
        ), 
            context=[user_context])

        flash('Thank you for your support!', 'success')
        return redirect('/')
    return render_template("donate.html")

if __name__ == '__main__':
    app.run()