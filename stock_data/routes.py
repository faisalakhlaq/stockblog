from datetime import datetime
from flask import render_template, request, flash
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# from get_all_tickers import get_tickers as gt

from stock_data import app
from stock_data.forms import StockDataForm
from stock_data.stock_analysis import StockAnalyzer
from stock_data.forms import CryptoFetcherForm
from stock_data.crypto import CoinMarket


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/stock_data', methods=['GET', 'POST'])
def stock_data():
    tickers = []
    with open("tickers.txt", mode='r') as file:
        for line in file.readlines():
            tickers.append(line)

    print(len(tickers))
    form = StockDataForm()
    if request.method == 'GET':
        return render_template("stock_data.html", list_of_tickers=tickers, form=form)
    elif request.method == 'POST':
        if not form.validate_on_submit() or \
                form.startdate.data > form.enddate.data or \
                form.startdate.data > datetime.date(datetime.now()):
            error_message = "Invalid Dates!"
            return render_template("stock_data.html", list_of_tickers=tickers,
                                   error_message=error_message, form=form)

        stock_ticker = (request.form.get('stock_ticker_list')).strip()
        start_date = form.startdate.data
        end_date = form.enddate.data
        data = StockAnalyzer().get_graph(stock_ticker, start_date, end_date)
        return render_template("stock_data.html", list_of_tickers=tickers,
                               script1=data[0], div1=data[1], cdn_js=data[2], form=form)


@app.route('/crypto_currency_data', methods=['GET', 'POST'])
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


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
