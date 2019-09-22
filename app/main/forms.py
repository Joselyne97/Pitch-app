from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField,RadioField
from wtforms.validators import Required,Email
from wtforms import ValidationError

class PitchForm(FlaskForm):
    title = StringField('title',validators=[Required()])
    description = TextAreaField("What would you like to pitch?",validators=[Required()])
    category = RadioField('Label', choices=[ ('pickup','pickup'), ('interview','interview'),('promotion','promotion'),('product','product')],validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()

class UpvoteForm(FlaskForm):
	submit = SubmitField()


class Downvote(FlaskForm):
	submit = SubmitField()
