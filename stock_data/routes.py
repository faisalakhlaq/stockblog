from datetime import datetime
from flask import render_template, request
from get_all_tickers import get_tickers as gt

from stock_data import app
from stock_data.forms import StockDataForm
from stock_data.stock_analysis import StockAnalyzer


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/stock_data', methods=['GET', 'POST'])
def stock_data():
    list_of_tickers = gt.get_tickers()
    # first_tickers = ['DDD', 'MMM', 'WBAI', 'EGHT', 'AHC', 'AOS', 'ATEN', 'AIR', 'AAN', 'ABB', 'ABT', 'ABBV', 'ANF', 'AGD', 'AWP', 'ACP', 'JEQ', 'ASGI', 'AOD', 'ABM', 'AKR', 'ACEL', 'ACN', 'ACCO', 'ATV', 'AYI', 'GOLF', 'ADX', 'PEO', 'ADCT', 'AGRO', 'ADNT', 'ADT', 'ATGE', 'AAP', 'ADSW', 'WMS', 'ASIX', 'AVK', 'ACM', 'AEFC', 'AEB', 'AEG', 'AER', 'AJRD', 'AMG', 'MGR', 'MGRB', 'AFL', 'MITT', 'AGCO', 'A', 'AEM', 'ADC', 'AL', 'APD', 'ALG', 'AGI', 'ALK', 'AIN', 'ALB', 'ACI', 'AA', 'ALC', 'ALEX', 'ALX', 'ARE', 'AQN', 'AQNA', 'AQNB', 'BABA', 'Y', 'ATI', 'ALLE', 'ALE', 'ADS', 'AFB', 'AWF', 'AB', 'AIO', 'CBH', 'NCV', 'NCZ', 'ACV', 'NFJ', 'NIE', 'ALSN', 'ALL', 'ALLY', 'PINE', 'ALTG', 'AYX', 'ATUS', 'MO', 'ACH', 'ALUS', 'AMBC', 'ABEV', 'AMC', 'AMCR', 'AEE']

    form = StockDataForm()
    if request.method == 'GET':
        return render_template("stock_data.html", list_of_tickers=list_of_tickers, form=form)
    elif request.method == 'POST':
        if not form.validate_on_submit() or \
                form.startdate.data > form.enddate.data or \
                form.startdate.data > datetime.date(datetime.now()):
            error_message = "Invalid Dates!"
            return render_template("stock_data.html", list_of_tickers=list_of_tickers,
                                   error_message=error_message, form=form)

        stock_ticker = request.form.get('stock_ticker_list')
        start_date = form.startdate.data
        end_date = form.enddate.data
        data = StockAnalyzer().get_graph(stock_ticker, start_date, end_date)
        return render_template("stock_data.html", list_of_tickers=list_of_tickers,
                               script1=data[0], div1=data[1], cdn_js=data[2], form=form)


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
