from datetime import datetime
from flask import render_template, request, Blueprint, flash
from flask_login import login_required
from sqlalchemy import desc
# from get_all_tickers import get_tickers as gt
from flask_login import current_user

from stock_data import db
from .forms import StockDataForm, StockTechnicalTermsForm
from .models import StockTechnicalTerms
from .stock_analysis import StockAnalyzer

stock = Blueprint('stock', __name__)


@stock.route('/')
@stock.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@stock.route('/stock_data', methods=['GET', 'POST'])
def stock_data():
    tickers = []
    with open("tickers.txt", mode='r') as file:
        for line in file.readlines():
            tickers.append(line)

    # print(len(tickers))
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


# TODO move the below to blog/routes
@login_required
@stock.route('/stock_terms_entry_form', methods=['GET', 'POST'])
def stock_terms_entry_form():
    form = StockTechnicalTermsForm()
    post_id = request.args.get('post_id') or None
    import pdb; pdb.set_trace()
    if post_id:
        post = StockTechnicalTerms.query.get(int(post_id))
        form = StockTechnicalTermsForm(obj=post)
    technical_terms = StockTechnicalTerms.query.order_by(desc('updated')).all()
    if request.method == 'POST':
        if request.form.get('clear') or request.form.get('refresh'):
            form = StockTechnicalTermsForm(None)
        elif request.form.get('edit'):
            technical_term_id = request.form.get('edit')
            # TODO check if we can filter this record from the above
            #  resultset (technical_terms). No need to query the DB again.
            #  technical_terms has this record already.
            # technical_term = technical_terms.filter_by(id=technical_term_id)[0]
            technical_term = StockTechnicalTerms.query.get(technical_term_id)
            if not technical_term:
                flash('Sorry an error occurred while trying to find this term. <br> Please try again later.')
            else:
                form = StockTechnicalTermsForm(
                    term_id=technical_term_id,
                    term_name=technical_term.term_name,
                    definition=technical_term.definition,
                    description=technical_term.description,
                    calculation_process=technical_term.calculation_process,
                )
        elif request.form.get('delete'):
            technical_term_id = request.form.get('delete')
            # TODO storming the DB. Filter technical_terms to get it.
            delete_technical_term = StockTechnicalTerms.query.get(technical_term_id)
            if not delete_technical_term:
                flash('Sorry an error occurred while trying to find this term. <br> Please try again later.')
            else:
                db.session.delete(delete_technical_term)
                db.session.commit()
                # books = StockTechnicalTerms.query.paginate(page=page, per_page=books_per_page)
                flash("Term deleted from the database!")
        elif request.form.get('search'):
            term_name_ = form.term_name.data
            if term_name_ and len(term_name_.strip()) > 0:
                # TODO order_by not working
                rs = StockTechnicalTerms.query.order_by(desc('updated')). \
                    filter(StockTechnicalTerms.term_name.ilike("%" + term_name_ + "%")).all()
                if len(rs) > 0:
                    technical_terms = rs
                else:
                    flash('Sorry no terms found with the given name!')
            else:
                flash('Please provide a term name! <br> Search is only performed on term name')
        elif request.form.get("update"):
            if form.validate_on_submit() and form.term_id.data:
                id_ = form.term_id.data
                update_technical_term = StockTechnicalTerms.query.get(id_)
                if not update_technical_term:
                    flash('Sorry unable to update the record. Please check the values.', 'error')
                else:
                    update_technical_term.term_name = form.term_name.data
                    update_technical_term.definition = form.definition.data or None
                    update_technical_term.description = form.description.data or None
                    update_technical_term.calculation_process = form.calculation_process.data or None
                    db.session.commit()
                    flash('Stock term updated')
            else:
                flash('Sorry unable to update the record. Please check the values.', 'error')
        elif request.form.get("add_new"):
            if form.validate_on_submit():
                try:
                    term_name = form.term_name.data
                    rs = StockTechnicalTerms.query.filter_by(term_name=term_name).first()
                    if rs:
                        error = 'Sorry! The term name already exists.'
                        # TODO the term name should not be unique.
                        # We should be able to enter more then one term name
                        flash(error)
                        return render_template(
                            'stock_terms_entry_form.html',
                            terms=technical_terms,
                            form=form
                        )
                    definition = form.definition.data
                    description = form.description.data
                    calculation_process = form.calculation_process.data
                    user_id = current_user.get_id()
                    data = StockTechnicalTerms(
                        term_name_=term_name,
                        definition_=definition,
                        description_=description,
                        calculation_process_=calculation_process,
                        user_id_=user_id,
                    )
                    db.session.add(data)
                    db.session.commit()
                    flash(f"Created a new term\n {term_name}")
                    return render_template(
                        "stock_terms_entry_form.html",
                        terms=technical_terms,
                        form=StockTechnicalTermsForm(None)
                    )
                except TypeError as error:
                    print(error)
                    err_msg = 'Unable to save the term. Please try again'
                    flash(err_msg)
                    return render_template(
                        'stock_terms_entry_form.html',
                        terms=technical_terms,
                        form=form
                    )
                # TODO display a message for 5 sec
    return render_template(
        "stock_terms_entry_form.html",
        terms=technical_terms,
        form=form
    )
