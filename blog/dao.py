import sqlite3
import os
from .models import User, AnonymousUser, Article, Comment
from . import utilities

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
    def get(cls, articleid, include_all=False):
        con = cls.get_connection()
        res = do_select(con, "SELECT articleid, title, message , keywords, date, userid FROM Articles WHERE articleid=?", [articleid])
        if res is None:
            return None
        title = res[1]
        message = res[2]
        keywords = res[3]
        date = res[4]
        userid = res[5]
        article = Article(articleid=articleid, title=title, message=message, keywords=keywords, date=date, userid=userid)
        if include_all:
            article.author = UserDAO.get(userid).username
        return article

    @classmethod
    def save(cls, article:Article):
        con = cls.get_connection()
        fields = ['title', 'message', 'keywords', 'date', 'userid']
        for field in fields:
            value = getattr(article, field)
            print(field, type(value), value)

        if article.articleid is None:
            with con:   
                new_id = do_insert(con, "INSERT INTO Articles(title, message , keywords, date, userid) VALUES(?, ?, ?, ?, ?)",[article.title, article.message, article.keywords, article.date, article.userid])
                article.articleid = new_id
        else:
            with con:
                do_update(con,"UPDATE Articles SET title=?, message=?, keywords=? , date=?, userid=? WHERE articleid=?", [article.title, article.message, article.keywords, article.date, article.userid, article.articleid])
    
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


# userid|username|....| #Users

# articleid|userid|title|...| #Articles

# ==> userid|username|...|articleid|title|...| #User x Articles

    @classmethod
    def get_all(cls, include_all=True):
        con = cls.get_connection()
        all_articles=[]
        if include_all == True:
            article_rows = do_select(con, "SELECT articleid, title, message , keywords, date, Articles.userid, username FROM Articles inner join Users on (Articles.userid=Users.userid)", fetchall=True)
        else:
            article_rows = do_select(con, "SELECT articleid, title, message , keywords, date, userid FROM Articles", fetchall=True)
        for article_row in article_rows:
            articleid = article_row[0]
            title = article_row[1]
            message = article_row[2]
            keywords = article_row[3]
            date = article_row[4]
            userid = article_row[5]
            article  = Article(articleid=articleid, title=title, message=message, keywords=keywords, date=date, userid=userid)
            if include_all == True:
                article.author = article_row[6]
            all_articles.append(article)
            
        return all_articles


class CommentDAO(DAO):  #author, message, date, commentid=None
    @classmethod
    def get(cls, commentid, include_all=False):
        con = cls.get_connection()
        res = do_select(con, "SELECT commentid, message, date, userid, articleid FROM Comments WHERE commentid=?", [commentid])
        if res is None:
            return None
        message = res[1]
        date = res[2]
        userid = res[3]
        articleid = res[4]
        comment = Comment(commentid=commentid, message=message, date=date, userid=userid, articleid=articleid)
        if include_all:
            comment.author = UserDAO.get(userid).author
        return comment

    @classmethod
    def save(cls, comment:Comment):
        con = cls.get_connection()
        
        if comment.commentid is None:
            with con:   
                new_id = do_insert(con, "INSERT INTO Comments(message, date, userid, articleid) VALUES(?, ?, ?, ?)",[comment.message, comment.date, comment.userid, comment.articleid])
                comment.commentid = new_id
        else:
            with con:
                do_update(con, "UPDATE Comments SET message=?, date=?, userid=?, articleid=? WHERE commentid=?", [comment.message, comment.date, comment.userid, comment.articleid, comment.commentid])
    
    @classmethod
    def delete(cls, comment):
        con = cls.get_connection()
        with con:
            if isinstance(comment, Comment):
                commentid = comment.commentid
                comment.commentid = None
            else:
                commentid = comment
            do_delete(con, "DELETE FROM Comments WHERE commentid=?", [commentid])
            
    @classmethod
    def get_all(cls, articleid=None, include_all=True):
        con = cls.get_connection()
        all_comments=[]
        if articleid is None:
            comment_rows = do_select(con, "SELECT commentid, message, date, userid, articleid FROM Comments ", fetchall=True)
        else:
            comment_rows = do_select(con, "SELECT commentid, message, date, userid, articleid FROM Comments WHERE articleid=?", [articleid], fetchall=True)
        for comment_row in comment_rows:
            commentid = comment_row[0]
            message = comment_row[1]
            date = comment_row[2]
            userid = comment_row[3]
            articleid = comment_row[4]
            comment  = Comment(commentid=commentid, message=message, date=date, userid=userid, articleid=articleid)
            all_comments.append(comment)
            if include_all:
                if userid is None:
                    comment.author = "Anonymous User"
                else:
                    comment.author = UserDAO.get(userid).username
        return all_comments


class HelperDAO(DAO):  
    @classmethod
    def userid_article(cls, article_id):
        con = cls.get_connection()
        userid_article_tuple = do_select(con, "SELECT userid FROM Articles WHERE articleid=?", [article_id])
        if userid_article_tuple is None:
            return None
        userid_article = userid_article_tuple[0]
        return userid_article

    @classmethod
    def userid_logged_in(cls, username):
        con = cls.get_connection()
        userid_tuple = do_select(con, "SELECT userid FROM Users WHERE username=?", [username])
        if userid_tuple is None:
            return None
        userid_logged_in = userid_tuple[0]
        print(userid_logged_in)
        return userid_logged_in

    @classmethod 
    def vgl(cls, article_id, username):
        if HelperDAO.userid_article(article_id) == HelperDAO.userid_logged_in(username):
            return True

        else:
            return False

    @classmethod
    def search(cls, search_keywords):
        """
        :param search_keywords: list of strings!
        returns: all matching articles (without repetition!)!
        """
        # title: 3-4x
        # tags/keywords 2x
        # text 1x
        
        matching_articles = []
        #print("sk1: ", search_keywords)
        for article in ArticleDAO.get_all():
            #print("art.kw: ", article.keywords)
            for keyword in search_keywords:
                if keyword in article.keywords and article not in matching_articles:
                    matching_articles.append(article)
                    print(matching_articles)
        return matching_articles
        
    @classmethod
    def userid_comment(cls, comment_id):
        con = cls.get_connection()
        userid_comment_tuple = do_select(con, "SELECT userid FROM Comments WHERE commentid=?", [comment_id])
        if userid_comment_tuple is None:
            return None
        userid_comment = userid_comment_tuple[0]
        return userid_comment

    