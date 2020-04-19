
## Blog Project!!!
1. Create a blog-project repository

1. Models:
    1. User
        - username
        - password
        - name
        - is_admin
        - is_logged_in # Does not belongs to the database and is used for the session.
        - userid
    1.  AnonymousUser:  # Anonymous user has the same fields as User but is never saved in the database!!!
        - username = None
        - password = None
        - name = "Anynymous"
        - is_admin = False
        - is_logged_in = False
        - userid = None
    1. Article:
        - title
        - message
        - keywords # To make it easy, keyowrds can be a string with values separated by a semi-colon (e.g. "Discord;Python;2020")
        - date
        - articleid
        -has a user id from author
    1. Comment
        - author (can be missing or a User)
        - message
        - date
        - commentid

1. Permissions:  
    A User can:  
        - Article:  
            - add a new article  
            - modify or delete his blogs  
        - Comment:  
            - add a new comment  
            - modify or delete his comments  
        - User(if is_admin is True):  
            - modify or delete a User  
            - modify or delete blogs  
            - modify or delete comments  
    An AnonymousUser (logged in is False) can:  
        - Comment:  
            - add a new comment  

1. Steps:
    1. Create the models
    1. Create the database schemas
        - (optional) Think about constraints: e.g What should happen when a user is deleted?
    1. Create the database access objects (DAO) to add/delete/save models
    1. Create the flask app        
    1. Create the User registration page
    1. Create the User login and logout pages
        - after a successfull login, informations from the user are loaded and the user is saved in the session
        - after a successfull logout, the user saved in the session is deleted
    1. Create Article pages
        - the page to add a new article
        - the page to list all articles
        - the page to view an article
            - create a section to list comments of an article
            - create a section to add a new comment on an article
            - create the add comment section on the article page
