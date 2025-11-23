from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired
from booksdb import BooksDB

class SearchWTF(FlaskForm):
    myoptions = [(None, "Choose your Search Type"), ('byAuthor','By Author'),('byTitle','By Title'),
                 ('byPublisher','By Publisher')]
    search_choice = SelectField("SearchChoice", choices=myoptions,validators=[DataRequired()] )

class ByAuthorIdWTF(FlaskForm):
    mydb = BooksDB()
    authors = mydb.getauthors()
    author_choice = SelectField("AuthorChoice", choices=authors)


class ByPublisherIdWTF(FlaskForm):
    pass

class ByTitleWTF(FlaskForm):
    # This will also need a stringfield for the words the user types
    pass

