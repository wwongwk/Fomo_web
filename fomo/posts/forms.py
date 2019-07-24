from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, InputRequired
from wtforms import StringField, TextAreaField, SubmitField, SelectField, SelectMultipleField, RadioField
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.html5 import DateTimeField
from wtforms_sqlalchemy.fields import QuerySelectField
from fomo.models import Venue

def get_venues():
    return Venue.query

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Post')
    picture = FileField('Cover Picture', validators=[ FileAllowed(['jpg','png'])])
    caption = TextAreaField('A Short Description', validators=[DataRequired()])
    start_date = DateTimeField('Start Date', id='datepick', validators=[ InputRequired()], format='%Y-%m-%d %H:%M')
    end_date = DateTimeField('End Date', id='datepick', validators=[ InputRequired() ], format='%Y-%m-%d %H:%M')
    venue = SelectField('Event Venue', validators=[DataRequired()], coerce=int )
    categories = SelectMultipleField('Event Category', coerce=int)
    
class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    picture = FileField('Cover Picture', validators=[FileAllowed(['jpg','png'])])   
    description = TextAreaField('A Short Description', validators=[DataRequired()])