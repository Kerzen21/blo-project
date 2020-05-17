import time

class User(object):
    def __init__(self, username, password , is_admin, is_logged_in, userid=None):
        self.username = username 
        self.password =  password 
        self.is_admin = is_admin 
        self.is_logged_in = is_logged_in
        self.userid = userid

    def __str__(self):
        return "User<" + str(self.userid) + ": " + str(self.username) + " " + str(self.password) + " - " + str(self.is_admin) + " - " + str(self.is_logged_in) + ">"
    def __repr__(self):
        return self.__str__()


### to look: class variables / class attributes
class AnonymousUser(object):
    def __init__(self, username = None, password = None, is_admin = None, is_logged_in = False, userid=None):
        self.username = username 
        self.password =  password 
        self.is_admin = is_admin 
        self.is_logged_in = is_logged_in
        self.userid = userid

    def __str__(self):
        return "AnonymousUser<" + str(self.userid) + ">"
    def __repr__(self):
        return self.__str__()
        

class Article(object):
    def __init__(self, title, message , keywords, userid, date, articleid=None): # Date in written in EU, e.g.: 13/04/2020
        self.title = title 
        self.message =  message 
        self.keywords = keywords 
        self.date = date 
        self.userid = userid
        self.articleid = articleid
        # author is not saved in the database!!!
        self.author = None

    def __str__(self):
        return "Article<" + str(self.articleid) + ": " + str(self.userid) + " - " + str(self.title) + " " + str(self.message) + " - " + str(self.keywords) + " - " + str(self.date) + ">"
    def __repr__(self):
        return self.__str__()


class Comment(object):
    def __init__(self, author, message, date,commentid=None): 
        self.author = author 
        self.message =  message 
        self.date = date
        self.commentid = commentid

    def __str__(self):
        return "Comment<" + str(self.commentid) + ": " + str(self.author) + " " + str(self.message) + " - " + str(self.date) + ">"
    def __repr__(self):
        return self.__str__()
    

