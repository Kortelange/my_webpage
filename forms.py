from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField

class QuickThoughtForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    submit = SubmitField(label="Add thought")

class BookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    short_review = StringField('short review')
    body = CKEditorField('body')
    rating = FloatField('rating')
    submit = SubmitField(label='Add book')