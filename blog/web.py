from flask import Flask, request, render_template, redirect, url_for, flash, session
from functools import wraps
app = Flask(import_name=__name__)
from . import models
from . import dao
import random
import string
import os
import time
import datetime 
from . import utilities

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
    #dao.UserDAO.save(admin)

#####
    import sqlite3   # Registration

    try:
        dao.UserDAO.save(admin)
    except sqlite3.IntegrityError:
        print("The user is already available in the database!!!")
#####



print(logindata)


LOGGED_IN_KEY = "IS_LOGGED_IN"


@app.route('/login', methods=["POST", "GET"])   #UserID nehmen, und damit übeerprüfen ob man in List.html editieren bzw. deleten darf. Falls article ID mit USer ID übereinstimmt, darf man! Mit comment weiter machen fallss fertig
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        dao.UserDAO.get_from_login(username, password)
        if  dao.UserDAO.get_from_login(username, password): 
        
            flash("Login succesfull")
            session[LOGGED_IN_KEY] = True   #sollte mit session.get geholt werden
            session["user"] = {"username" : username, "userid" : dao.HelperDAO.userid_logged_in(username), "is_admin" : dao.UserDAO.get(dao.HelperDAO.userid_logged_in(username)).is_admin}
            print(request.args, "but going back to the homepage")
            next_url = request.args.get("next", "/")


            return redirect(next_url)
        else:
            flash("Username or Password invalid")
        return redirect(url_for("login", **request.args))

#print(session["user"]["is_admin"])

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")     #Fertig machen und dann mit dao.USerDAO.save(User) in der DB speichern TODO:
    else:
        username = request.form.get("username", "")
        password1 = request.form.get("password1", "")
        password2 = request.form.get("password2", "")
        import sqlite3
        if password1 == password2:   
            try: 
                user = models.User(username, password1, is_logged_in = False, is_admin = False)
                dao.UserDAO.save(user)
                session[LOGGED_IN_KEY] = False
                flash("Registration succesfull")
                
                return redirect(url_for("login", **request.args))
            except sqlite3.IntegrityError:
                    flash("The user is already available in the database!!!")
                    return render_template("register.html")
        else:
            flash("The Passwords do not match!")
            return redirect("/register")


if dao.HelperDAO.userid_logged_in("Super-Admin") is  None:
    super_admin = models.User("Super-Admin", "123", is_logged_in = False, is_admin = True) # Which element is not unique?
    dao.UserDAO.save(super_admin)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get(LOGGED_IN_KEY, False):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/articles/list", methods=["GET"])
def articles_list():
    return render_template("articles/list.html", articles = dao.ArticleDAO.get_all(), dao = dao)


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
        userid = dao.HelperDAO.userid_logged_in(session["user"]["username"])
        title = request.form.get("title", "")
        message = request.form.get("message", "")
        separator = ", "
        keywords = separator.join(utilities.key_word_finder(message))
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
        
        article = models.Article(title, message, keywords, userid, str(date))
        dao.ArticleDAO.save(article)
        flash(f"The Article has been posted!")
        flash(session["user"]["is_admin"])

        print(request.form) 
        return redirect("/articles/list")


# web-browser --> get-method --> user input --> post-method --> final-result

@app.route("/articles/search", methods=["GET", "POST"])
def search_article():
    if request.method == "GET":
        keywords = request.form.get("keywords", "")
        print("Keywords in GET: ", keywords)
        return render_template("articles/search.html")
    else:
        keywords = request.form.get("keywords", "")
        print("Keywords in POST: ", keywords)
        print(keywords.split(" "))
        matching_articles = dao.HelperDAO.search(keywords.split(" "))
        print(matching_articles)
        return render_template("articles/search.html", matching_articles = matching_articles)

        

@app.route("/articles")
@login_required
def articles_index():
    return render_template("articles/base.html")


#ICh suche: haus auto katze miete
#1. Artikel: 15x Haus 15x Auto
#3. Artikel: 10x Haus x Auto
#2. Artikel: 5x (Haus auto katze miete)


@app.route("/articles/<int:articleid>/edit", methods=["GET", "POST"])
@login_required       
def user_edit_article(articleid):
    
    if request.method == "GET":
        return render_template("articles/edit.html", article=dao.ArticleDAO.get(articleid))
    else: 

        article = dao.ArticleDAO.get(articleid)
        article.title = request.form.get("title", "")
        article.message = request.form.get("message", "")
        article.keywords = request.form.get("keywords", "")

        
        

        
        print("Article Nach Hinzufügung zu Models", article.userid)
        if dao.HelperDAO.vgl(articleid, session["user"]["username"]):
            dao.ArticleDAO.save(article)
            flash(f"The Article with id <{articleid}> has been edited!")
            return redirect("/articles/list")
        else:
            flash(f"The Article with id <{articleid}> is not yours!") 
        return redirect("/articles/list")
#Statt zu speicehern wird ein Neuer erstellt, also 165+ anschauen!




@app.route("/articles/delete")       
@login_required
def articles_delete():
    articleid = request.args.get("id")
    if 'confirmation' in request.args:
        article = dao.ArticleDAO.get(articleid)
        if dao.HelperDAO.vgl(articleid, session["user"]["username"]) or session["user"]["is_admin"]:
            dao.ArticleDAO.delete(article)
            flash(f"The Article with id <{articleid}> has been deleted!")
            return redirect("/articles/list")
        else:
            flash(f"The Article with id <{articleid}> is not yours!") 
            return redirect("/articles/list")
    else:
        return render_template("articles/delete.html", articleid=articleid)





@app.route("/articles/<int:articleid>/view/comments/add", methods=["GET", "POST"])   #ADDD COMMENT FERTIG MACHEN
def user_add_comment(articleid):
    if request.method == "GET": 
        return render_template('/comments/add.html')
    else:
        # should extract username from the session / user in the session login
        if "user" in session:
            userid = dao.HelperDAO.userid_logged_in(session["user"]["username"])
        else:
            userid = None
        message = request.form.get("message", "")
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
        
        comment = models.Comment(message, str(date), userid, articleid)
        dao.CommentDAO.save(comment)
        flash(f"The Comment has been posted!")
        print(request.form) 
        return redirect("/articles/" + str(articleid) + "/view")

@app.route("/articles/<int:articleid>/view/comments/<int:commentid>/edit", methods=["GET", "POST"])
@login_required       
def user_edit_comment(articleid, commentid):
    
    if request.method == "GET":
        return render_template("comments/edit.html", article=dao.ArticleDAO.get(articleid) , comment=dao.CommentDAO.get(commentid))
    else: 

        comment = dao.CommentDAO.get(commentid)
        comment.message = request.form.get("message", "")

        
        

        if dao.HelperDAO.userid_comment(commentid) == dao.HelperDAO.userid_logged_in(session["user"]["username"]):
            dao.CommentDAO.save(comment)
            flash(f"The Comment with id <{commentid}> has been edited!")
            return redirect("/articles/list")
        else:
            flash(f"The Comment with id <{commentid}> is not yours!") 
            return redirect("/articles/" + str(articleid) + "/view/comments/")



  
@app.route("/articles/<int:articleid>/view/comments/<int:commentid>/delete", methods=["GET", "POST"])      
@login_required
def comment_delete(articleid, commentid):
    if request.method == "GET":
        return render_template("comments/delete.html", article=dao.ArticleDAO.get(articleid), comment = dao.CommentDAO.get(commentid))
    else:
        comment = dao.CommentDAO.get(commentid)
        is_comment_author = dao.HelperDAO.userid_comment(commentid) == dao.HelperDAO.userid_logged_in(session["user"]["username"])
        is_article_author = dao.HelperDAO.userid_article(articleid) == dao.HelperDAO.userid_logged_in(session["user"]["username"])
        if is_comment_author or is_article_author or  session["user"]["is_admin"]: 
                dao.CommentDAO.delete(comment)
                flash(f"The Comment with id <{commentid}> has been deleted!")
        else:
            flash(f"The Comment with id <{commentid}> is not yours!")
        return redirect("/articles/" + str(articleid) + "/view")



@app.route("/articles/<int:articleid>/view", methods=["GET", "POST"])
def article_view(articleid):
    if request.method == "GET":
        article = dao.ArticleDAO.get(articleid)
        # article.score = 23324
        article_score = dao.VoteDAO.get_score_article(articleid)
        comments = dao.CommentDAO.get_all(articleid, True)
        print(comments)
        return render_template("/articles/view.html", article=article, comments=comments, article_score=article_score)


#Comment<1: Tim     Tester 1 - 03/07/2020 - 0>



@app.route("/articles/<int:articleid>/view/upvote", methods=["GET", "POST"])      
@login_required
def upvote_article(articleid):
    if request.method == "GET":
        return render_template("articles/upvote.html", article=dao.ArticleDAO.get(articleid))
    else:
        dao.VoteDAO.user_vote_article(dao.HelperDAO.userid_logged_in(session["user"]["username"]), articleid, True)
        return redirect("/articles/" + str(articleid) + "/view")

@app.route("/articles/<int:articleid>/view/downvote", methods=["GET", "POST"])      
@login_required
def downvote_article(articleid):
    if request.method == "GET":
        return render_template("articles/downvote.html", article=dao.ArticleDAO.get(articleid))
    else:
        #NOTE
        dao.VoteDAO.user_vote_article(dao.HelperDAO.userid_logged_in(session["user"]["username"]), articleid, False)
        return redirect("/articles/" + str(articleid) + "/view")






@app.route("/articles/<int:articleid>/view/comments/<int:commentid>/upvote", methods=["GET", "POST"])      
@login_required
def upvote_comment(articleid, commentid):
    if request.method == "GET":
        return render_template("comments/upvote.html", article=dao.ArticleDAO.get(articleid), comment=dao.CommentDAO.get(commentid))
    else:
        dao.VoteDAO.user_vote_comment(dao.HelperDAO.userid_logged_in(session["user"]["username"]), commentid, True)
        return redirect("/articles/" + str(articleid) + "/view")


@app.route("/articles/<int:articleid>/view/comments/<int:commentid>/downvote", methods=["GET", "POST"])      
@login_required
def downvote_comment(articleid, commentid):
    if request.method == "GET":
        return render_template("comments/downvote.html", article=dao.ArticleDAO.get(articleid), comment=dao.CommentDAO.get(commentid))
    else:
        dao.VoteDAO.user_vote_comment(dao.HelperDAO.userid_logged_in(session["user"]["username"]), commentid, False)
        return redirect("/articles/" + str(articleid) + "/view")





@app.route("/logout")      
def logout():
     session.clear()
     flash("Succesfully logged out")
     return redirect("/")


if __name__ == "__main__":
    app.run(threaded=False, processes=1, debug=True)