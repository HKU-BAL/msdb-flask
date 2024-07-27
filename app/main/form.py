from flask_wtf import FlaskForm
from wtforms import TextAreaField,StringField, SubmitField
from wtforms.validators import DataRequired,Email,Optional,Length


class searchForm(FlaskForm):

    search_key_words= StringField("Search mitronDB-BAL-HKU database...",validators=[Optional()]) 
    submit = SubmitField('Search')


class downloadForm(FlaskForm):


    submit = SubmitField("Download")
    pass


class contactForm(FlaskForm):



    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name',validators=[DataRequired()])
    question = TextAreaField('Question', validators=[DataRequired(),Length(max=1000, message="Question must be 1000 characters or less.")])
    title = StringField('Title', validators=[Optional()])
    submit = SubmitField("Send")
    pass




