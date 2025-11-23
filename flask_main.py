from flask import Flask, render_template, request, url_for, redirect, session
from string import Template
from loginwtf import LoginWTF
from searchwtf import SearchWTF,ByAuthorIdWTF
from booksdb import BooksDB
from flask_session import Session
from flask_bcrypt import Bcrypt
from wtforms import StringField, TextAreaField, DateField,DecimalField,FloatField,IntegerField,RadioField,SelectField
from wtforms import HiddenField,PasswordField

app = Flask(__name__)
bcrypter = Bcrypt(app)

SESSION_TYPE = 'filesystem'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True # Need https for this to be remotely true
app.secret_key = b'(YPT#{@#YAS^RPPF#TA#DGA#adsg' # This should be protected ie don't record it on zoom ;)
app.config.from_object(__name__)
Session(app)

@app.route("/")
def index():
    return "Hello World"


@app.route("/aboutme")
def aboutme():
    return "You probably think this song is about you"


@app.route('/greeting')
@app.route('/greeting/<username>')
def sayhello(username=None):
    if username is not None:
        return Template("Hello there $name").substitute(name=username)
    else:
        return "Hello whoever you are!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['status'] = False
    # request.method will only = "POST" if the form has been submitted)
    if request.method == 'POST':
        # are you totally insane! THIS IS HORRIBLY INSECURE!!!!!
        user = request.form['username']
        passwd = request.form['secret']
        if passwd == "Password1234":
            session['status'] = True
        return "Username: {0} <br />Password: {1}".format(user,passwd)
    else:
        #form has not been submitted if it is a GET in this case
        return render_template('loginform.html')

@app.route('/logout')
def logthemout():
    session['status'] = False
    return "You have logged out, try the <a href=\"/admin\">Administrator Page</a>"

@app.route('/admin')
def administrator():
    if session['status'] == True:
        return "Welcome Administator!"
    else:
        return redirect('/login')

@app.route('/data')
def exampledata():
    mytitle = "This is a cool title"
    userdict = [{'fname': 'Phil', 'lname': 'Waclawski'},
                {'fname': 'Doug', 'lname': 'Waclawski'},
                {'fname': 'Randy', 'lname': 'Waclawski'},
                {'fname': 'Robbie', 'lname': 'Waclawski'},
                {'fname': 'Becky', 'lname': 'Waclawski'},
                {'fname': 'Keith', 'lname': 'Waclawski'},
                {'fname': 'Aaron', 'lname': 'Waclawski'}
                ]
    return render_template('dataexamples.html', title=mytitle, data=userdict)

@app.route('/testbcrypt')
def btester():
    passtotest = ')*P%T:*O$TW$'
    hashpass = bcrypter.generate_password_hash(passtotest, 16).decode('utf-8')

    # To check to see if the password they just entered is correct
    # you retrieve the hash, send that AND the password to check
    # Bcrypt uses that information to hash the password entered
    # and returns true if the new hash matches the old one

    if bcrypter.check_password_hash(hashpass, passtotest):
        return f"That was the same password {hashpass}"
    else:
        return f"That was NOT the same password"


@app.route('/loginwtf', methods=['GET',"POST"])
def login_wtf():
    loginform = LoginWTF()
    if loginform.validate_on_submit():
        return "Form Submitted"
    return render_template('loginwtf.html',form=loginform)

"""
********************************************************
The sections below are your work area 
********************************************************
"""

@app.route('/search', methods=['GET','POST'])
def searchchoices():
    searchform = SearchWTF()
    if searchform.validate_on_submit():
        if request.form['search_choice'] == None:
            # This does not seem to work right at this point
            # But as long as user does pick a search type, the else: works fine
            return redirect('/')
        else:
            return search_router(request.form['search_choice'])
    return render_template('mainsearch.html',form=searchform)


# note, just a helper function, not used as a route
def search_router(searchtype):
    if searchtype == 'byAuthor':
        byauthorform = ByAuthorIdWTF()
        return render_template('byauthor.html', form=byauthorform)
    elif searchtype == 'byTitle':
        return "You Choose by Title"
    elif searchtype == 'byPublisher':
        return "You Choose by Publisher"


@app.route('/results/<option>', methods=['POST'])
def search_results(option=None):
    if option is None:
        return "Something went wrong"
    elif option == "booksbyauthorid":
        mydb = BooksDB()
        books = mydb.getbooksbyauthorid(request.form['author_choice'])
        return render_template('booksbyauthorid.html', data=books)
    elif option == "booksbypublisherid":
        return "Should list books by publisherid"
    elif option == "booksbytitle":
        return "Should list books by title"




if __name__ == "__main__":
    app.run()
