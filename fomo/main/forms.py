from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user

class testForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    test = StringField('')
    submit = SubmitField('Post')