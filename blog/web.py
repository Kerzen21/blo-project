from flask import Flask, request, render_template, redirect, url_for, flash, session
from functools import wraps
app = Flask(import_name=__name__)
from . import models
from . import dao
import random
import string
import os

def randomString(stringLength=20):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

env = os.environ
key = "BLOG_SECRET_KEY"
app.config["SECRET_KEY"] = randomString()
if key in env:
    if env[key] != "":
        app.config["SECRET_KEY"] = env[key]

def get_hash(message):
    base = 31
    for c in message:
        base *= ord(c)
    
    base %= 1000000000
    return str(base)


admin_pwd = os.environ.get("ADMIN_PASSWORD")
logindata = dict()
if admin_pwd:
    logindata["Tim"] = get_hash(admin_pwd)

print(logindata)


LOGGED_IN_KEY = "IS_LOGGED_IN"


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in logindata:
            if logindata[username] == get_hash(password):
                flash("Login succesfull")
                session[LOGGED_IN_KEY] = True
                print(request.args, "but going back to the homepage")
                next_url = request.args.get("next", "/")
                # if next is not None:
                #     return redirect(request.args["next"])
                return redirect(next_url)
            else:
                flash("Username or Password invalid")
        else:
            flash("Username or Password invalid")
        return redirect(url_for("login", **request.args))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get(LOGGED_IN_KEY, False):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html", my_variable="1024")

#User:
@app.route("/add-article", methods=["GET", "POST"])
@login_required
def user_add_article():
    if request.method == "GET": 
        users = []
        for user in dao.UserDAO.get_all():
            users.append(user)
            print(users)
        return render_template('/add-article.html', users=users)
    else:
        subjectid = request.form.get("subjid", "")
        studentid = request.form.get("sdtid", "")
        grade_grade = request.form.get("grade", "")
        grade = models.Grade(subjectid, studentid, grade_grade)
        dao.GradeDAO.save(grade)
        flash(f"The Grade has been added!")
        print(request.form) 
        return redirect("/grades") 