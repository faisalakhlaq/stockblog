from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class StockDataForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(DataRequired(),))
    submit = SubmitField('Fetch Stock Data')


