from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError


class StockDataForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(DataRequired(),))
    submit = SubmitField('Fetch Stock Data')


class AmountIntValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u'Amount must be an integer value greater than 0.'
        self.message = message

    def __call__(self, form, field):
        if not field.data or not isinstance(field.data, int) or int(field.data) == 0:
            raise ValidationError(self.message)


class CryptoFetcherForm(FlaskForm):
    currency_symbol = StringField('Crypto Currency Symbol', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[AmountIntValidator()])
    add_currency = SubmitField('Add Currency')
    currencies = TextAreaField('Added Currencies')
    # currencies = TextAreaField('Added Currencies', render_kw={'class': 'currencies-textarea', 'rows': 5})
    clear_currencies = SubmitField('Clear Currencies')
    fetch_data = SubmitField('View Portfolio')

