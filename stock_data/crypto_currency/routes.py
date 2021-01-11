from flask import render_template, request, flash, Blueprint
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from .forms import CryptoFetcherForm
from .crypto import CoinMarket

crypto = Blueprint('crypto', __name__)


@crypto.route('/crypto_currency_data', methods=['GET', 'POST'])
def crypto_currency_data():
    form = CryptoFetcherForm()
    crypto_symbols = list(CoinMarket().get_cur_symol_id().values())
    if request.method == 'POST':
        if form.clear_currencies.data:
            form.currencies.data = None
        elif form.add_currency.data:
            if form.validate_on_submit():
                symbol = form.currency_symbol.data
                form.currency_symbol.data = None
                amount = form.amount.data
                form.amount.data = ''
                form.currencies.data = str(form.currencies.data) + \
                                       str(symbol) +'-'+ str(amount) + '\n'
        elif form.fetch_data.data:
            # 1. Get the currencies from textarea
            # 2. Check if they are valid or send directly if the api won't crash with wrong symbols
            # 3. Put the returned data in a tabular form
            txtarea = form.currencies.data
            if txtarea is not None and len(txtarea.strip()) > 0:
                amount = txtarea.split()
                currencies = {}
                seperator = '-'
                for cur in amount:
                    k = cur.split(seperator, 1)
                    # v = cur.split(seperator, 1)[1]
                    currencies[str(k[0]).upper()] = k[1]
                try:
                    data = CoinMarket().get_crypto_portfolio(currencies)
                    return render_template('crypto_fetcher.html', form=form,
                                           list_data=data, crypto_symbols=crypto_symbols)
                except (ConnectionError, Timeout, TooManyRedirects, ValueError) as e:
                    flash(str(e)) # TODO FIXME not being displayed
                    print(e)
    return render_template('crypto_fetcher.html', form=form,
                           crypto_symbols=crypto_symbols)
