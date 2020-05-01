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
#TODO: admin_password is connected with username admin
if admin_pwd:
    logindata["Tim"] = get_hash(admin_pwd)
    #testpersona:
    admin = models.User("Tim", admin_pwd, True, False)
    dao.UserDAO.save(admin)

#####
    import sqlite3   # Registration

    try:
        dao.UserDAO.save(admin)
    except sqlite3.IntegrityError:
        print("The user is already available in the database!!!")
#####



print(logindata)


LOGGED_IN_KEY = "IS_LOGGED_IN"



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        dao.UserDAO.get_from_login(username, password)
        if  dao.UserDAO.get_from_login(username, password): 
        
            flash("Login succesfull")
            session[LOGGED_IN_KEY] = True
            print(request.args, "but going back to the homepage")
            next_url = request.args.get("next", "/")

            return redirect(next_url)
        else:
            flash("Username or Password invalid")
        return redirect(url_for("login", **request.args))


@app.route('/register')
def register():
    if request.method == "GET":
        return render_template("register.html")     #Fertig machen und dann mit dao.USerDAO.save(User) in der DB speichern TODO:
    else:
        username = request.form.get("username", "")
        password1 = request.form.get("password1", "")
        password2 = request.form.get("password2", "")
    #     import sqlite3   # Registration
#
    #try:
    #    dao.UserDAO.save(admin)
    #except sqlite3.IntegrityError:
    #    print("The user is already available in the database!!!")
#

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
@app.route("/articles/add", methods=["GET", "POST"])
@login_required
def user_add_article():
    if request.method == "GET": 
        users = []
        for user in dao.UserDAO.get_all():
            users.append(user)
            print(users)
        return render_template('/articles/add.html', users=users)
    else:
        # should extract username from the session / user in the session login
        logindata = request.form.get("username", "")
        title = request.form.get("title", "")
        message = request.form.get("message", "")
        keywords = request.form.get("keywords", "")
        article = models.Article(logindata, title, message, keywords)
        dao.ArticleDAO.save(article)
        flash(f"The Article has been posted!")
        print(request.form) 
        return redirect("/articles/list")

# /articles/1
# [title], [author],[date]
# [message]
# [
#     comment1,
#     comment2,
#     ...
# ]


@app.route("/articles")
@login_required
def articles_index():
    return render_template("articles/base.html")



@app.route("/articles/<int:articleid>/edit", methods=["GET", "POST"])
@login_required       
def user_edit_article(articleid):
    if request.method == "GET":
        return render_template("articles/edit.html", article=dao.ArticleDAO.get(articleid))
    else: 
        article_id = request.form.get("id", "")
        article_title = request.form.get("title", "")
        article_message = request.form.get("message", "")
        article_keywords = request.form.get("keywords", "")
        article = models.Student(article_title, article_message, article_keywords, article_id)
        dao.StudentDAO.save(article)
        flash(f"The Article with id <{article_id}> has been edited!") 
        return redirect("/articles/list")

@app.route("/articles/delete")       
@login_required
def articles_delete():
    articleid = request.args.get("id")
    if 'confirmation' in request.args:
        article = dao.ArticleDAO.get(articleid)
        dao.ArticleDAO.delete(article)
        flash(f"The Article with id <{articleid}> has been deleted!")

        return redirect("/articles/list")
    else:
        return render_template("articles/delete.html", articleid=articleid)


if __name__ == "__main__":
    app.run(threaded=False, processes=1, debug=True)