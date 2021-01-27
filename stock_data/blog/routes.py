from flask import render_template, request, Blueprint, flash
from sqlalchemy import desc

from stock_data.stock_app.models import StockTechnicalTerms

blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/blog_home', methods=['GET', 'POST'])
def blog_home():
    posts = StockTechnicalTerms.query.order_by(desc('updated')).all()
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        if request.form.get('refresh'):
            pass
        elif request.form.get('query'):
            term_name_ = request.form.get('query')
            if term_name_ and len(term_name_.strip()) > 0:
                rs = StockTechnicalTerms.query.filter(StockTechnicalTerms.term_name.ilike("%" + term_name_ + "%")).all()
                if len(rs) > 0:
                    posts = rs
                else:
                    flash('Sorry no terms found with the given name!')
            else:
                flash('Please provide a name!')
    return render_template('blog_home.html', posts=posts)
