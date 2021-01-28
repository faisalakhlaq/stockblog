from flask import render_template, request, Blueprint, flash, redirect, url_for
from sqlalchemy import desc

from stock_data.stock_app.models import StockTechnicalTerms

blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/blog', methods=['GET', 'POST'])
def blog_home():
    posts = StockTechnicalTerms.query.order_by(desc('updated')).all()
    if request.method == 'POST':
        if request.form.get('refresh'):
            pass
        elif request.form.get('query'):
            term_name_ = request.form.get('query')
            if term_name_ and len(term_name_.strip()) > 0:
                rs = StockTechnicalTerms.query.filter(StockTechnicalTerms.term_name.ilike("%" + term_name_ + "%")).all()
                if len(rs) > 0:
                    posts = rs
                else:
                    flash('Sorry no terms found with the given search text!', 'info')
            else:
                flash('Please provide a search text!', 'warning')
    return render_template('blog_home.html', posts=posts)


@blog.route('/post/<int:pid>', methods=['GET'])
def post(pid):
    blog_post = StockTechnicalTerms.query.get(pid)
    if not blog_post:
        flash('Sorry post cannot be found!<br>Redirecting to blog home page.', 'info')
        return redirect(url_for('blog.blog_home'))
    posts = StockTechnicalTerms.query.order_by(desc('updated')).all()
    return render_template('post.html', post=blog_post, posts=posts)
