from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class EditAmateurForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=0, max=64)])
    tw = StringField('tw', validators=[Length(min=0, max=15)])
    mdhId = StringField('mdhId', validators=[Length(min=0, max=30)])
    vxId = StringField('vxId', validators=[Length(min=0, max=30)])
    pmId = StringField('pmId', validators=[Length(min=0, max=30)])
    subDomain = StringField('subDomain', validators=[Length(min=0, max=30)])