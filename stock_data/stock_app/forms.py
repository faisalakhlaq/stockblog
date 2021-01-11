from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, StringField, TextAreaField, IntegerField
from wtforms.validators import (DataRequired, Length, Optional)


class StockDataForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(DataRequired(),))
    submit = SubmitField('Fetch Stock Data')


class StockTechnicalTermsForm(FlaskForm):
    term_id = IntegerField('id', validators=[Optional()])
    term_name = StringField(validators=[DataRequired("please enter a term"),
                                        Length(min=2, max=255,
                                        message='Length is 3-255 characters')])
    definition = TextAreaField(validators=[Length(min=0, max=255,
                                                  message='Length is 0-255 characters')])
    description = TextAreaField(validators=[Length(min=0, max=500,
                                                  message='Length is 0-255 characters')])
    calculation_process = TextAreaField(validators=[Length(min=0, max=500,
                                                  message='Length is 0-255 characters')])
    add_new = SubmitField('Add New')
    clear = SubmitField('Clear')
    search = SubmitField('Search')
    update = SubmitField('Update')
    delete = SubmitField(label='Delete')
    edit = SubmitField('Edit')
    refresh = SubmitField('Refresh')
