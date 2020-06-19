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
        # self.upvotes = [(2, 2, 1,)]
        # self.downvotes = [(1, 2, 2,)]

    def __str__(self):
        return "Article<" + str(self.articleid) + ": " + str(self.userid) + " - " + str(self.title) + " " + str(self.message) + " - " + str(self.keywords) + " - " + str(self.date) + ">"
    def __repr__(self):
        return self.__str__()


class Comment(object):
    def __init__(self, message, date, userid, articleid, commentid=None): 
        self.author = None 
        self.message =  message 
        self.date = date
        self.userid = userid
        self.articleid = articleid
        self.commentid = commentid

    def __str__(self):
        return "Comment<" + str(self.commentid) + ": " + str(self.author) + " " + str(self.message) + " - " + str(self.date) + ">"
    def __repr__(self):
        return self.__str__()
    

class Vote(object):
    def __init__(self, userid, upvote=None, downvote=None, articleid=None, commentid=None): #Upvote/Downvote is Bolean | Article/Commentid is IDs
        self.userid = userid
        self.upvote = upvote
        self.downvote = downvote
        self.articleid = articleid
        self.commentid = commentid
    def __str__(self):
        return "Vote<" + str(self.userid) + ":" + str(self.upvote) + "/" + str(self.downvote) + "|" + str(self.articleid) + "/" + str(self.commentid) + ">"
    def __repr__(self):
        return self.__str__()    