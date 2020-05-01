import sqlite3
import os
from .models import User, AnonymousUser, Article, Comment

db_filename = "database.sqlite3"    


blog_path = __file__

blog_split = []

blog_split = blog_path.split(os.path.sep)
blog_split.pop(-1)
blog_split.append("blog.sql")
seperator = os.path.sep
blog_final_path = seperator.join(blog_split)


db_create_script = str(blog_final_path)

def get_db_connection(db_filename):
    return sqlite3.connect(db_filename, check_same_thread=False)


class DBManager(object):
    _con: sqlite3.Connection = None
    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._con is None:
            cls._con = get_db_connection(db_filename)

            with open(db_create_script) as blog_file:
                blog_script = blog_file.read()

            blog = cls._con.executescript(blog_script)
        return cls._con

def do_update(con, sql, params):  
    con.execute(sql, params)
def do_insert(con, sql, params): 
    con.execute(sql, params)
    id_row = con.execute("select last_insert_rowid()").fetchone()
    new_id = id_row[0]
    return new_id
def do_delete(con, sql, params):  
    con.execute(sql, params)
def do_select(con, sql, params=None, fetchall=None):  
    if params is None:
        params = []
    if fetchall:
        res = con.execute(sql, params).fetchall()   # [ (teacherid, name, ...), (teacherid, name, ...)]
        return res 
    else:
        res = con.execute(sql, params).fetchone()   
        return res


class DAO(object): #Data access object
    
    @classmethod
    def get(cls, id_):
        # Return the object with the corresponding id_
        pass

    @classmethod
    def get_all(cls):
        # Return all objects
        pass

    @classmethod
    def save(cls, obj):
        # save the obj into the database and update its id if required
        pass

    @classmethod
    def delete(cls, obj):
        # delete the obj from the database and set it's id to None
        pass 
    
    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        return DBManager.get_connection()

class UserDAO(DAO):  #dao.UserDAO.get_from_login(username, password) für Web.py
    @classmethod
    def get(cls, userid):
        con = cls.get_connection()
        res = do_select(con, "SELECT userid , username, password, is_admin, is_logged_in FROM Users WHERE userid=?", [userid])
        if res is None:
            return None
        username = res[1]
        password = res[2]
        is_admin = res[3]
        is_logged_in = res[4]
        user = User(userid=userid, username=username, password=password, is_admin=is_admin, is_logged_in=is_logged_in)
        return user

    @classmethod
    def save(cls, user:User):
        con = cls.get_connection()
        if user.userid is None:
            with con:   
                new_id = do_insert(con, "INSERT INTO Users(username, password, is_admin, is_logged_in) VALUES(?, ?, ?, ?)",[user.username, user.password, user.is_admin, user.is_logged_in])
                user.userid = new_id
        else:
            with con:
                do_update(con,"UPDATE Users SET username=?, password=?, is_admin=? , is_logged_in=? WHERE userid=?", [user.username, user.password, user.is_admin, user.is_logged_in, user.userid])
    
    @classmethod
    def delete(cls, user):
        con = cls.get_connection()
        with con:
            if isinstance(user, User):
                userid = user.userid
                user.userid = None
            else:
                userid = user
            do_delete(con, "DELETE FROM Users WHERE userid=?", [userid])

    @classmethod
    def get_all(cls):
        con = cls.get_connection()
        all_users=[]
        user_rows = do_select(con, "SELECT userid, username, password, is_admin, is_logged_in FROM Users", fetchall=True)
 
        for user_row in user_rows:
            userid = user_row[0]
            username = user_row[1]
            password = user_row[2]
            is_admin = user_row[3]
            is_logged_in = user_row[4]

            user  = User(userid=userid, username=username, password=password, is_admin=is_admin, is_logged_in=is_logged_in)
            all_users.append(user)
        return all_users

    @classmethod
    def get_from_login(cls, username, password):
        con = cls.get_connection()
        res = do_select(con, "SELECT username, password FROM Users WHERE username=?", [username])
        if res is None:
            return False
        else:
            res_password = res[1]
            if password == res_password:
                return True
            else:
                return False

        

class ArticleDAO(DAO):  #articleid, title, message , keywords, date
    @classmethod
    def get(cls, articleid):
        con = cls.get_connection()
        res = do_select(con, "SELECT articleid, title, message , keywords, date FROM Articles WHERE articleid=?", [articleid])
        if res is None:
            return None
        title = res[1]
        message = res[2]
        keywords = res[3]
        date = res[4]
        article = Article(articleid=articleid, title=title, message=message, keywords=keywords, date=date)
        return article

    @classmethod
    def save(cls, article:Article):
        con = cls.get_connection()
        if article.articleid is None:
            with con:   
                new_id = do_insert(con, "INSERT INTO Articles(title, message , keywords, date) VALUES(?, ?, ?, ?)",[article.title, article.message, article.keywords, article.date])
                article.articleid = new_id
        else:
            with con:
                do_update(con,"UPDATE Articles SET title=?, message=?, keywords=? , date=? WHERE articleid=?", [article.title, article.message, article.keywords, article.date])
    
    @classmethod
    def delete(cls, article):
        con = cls.get_connection()
        with con:
            if isinstance(article, Article):
                articleid = article.articleid
                article.articleid = None
            else:
                articleid = article
            do_delete(con, "DELETE FROM Articles WHERE articleid=?", [articleid])

    @classmethod
    def get_all(cls):
        con = cls.get_connection()
        all_articles=[]
        article_rows = do_select(con, "SELECT title, message , keywords, date FROM Articles", fetchall=True)
        for article_row in article_rows:
            articleid = article_row[0]
            title = article_row[1]
            message = article_rows[2]
            keywords = article_rows[3]
            date = article_row[4]

            article  = Article(articleid=articleid, title=title, message=message, keywords=keywords, date=date)
            all_articles.append(article)
        return all_articles
        
        