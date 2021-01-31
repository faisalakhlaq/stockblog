from flask import (render_template, request, Blueprint,
                   flash, redirect, url_for, abort)
from flask_login import current_user, login_required
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


@blog.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    current_post = StockTechnicalTerms.query.get(post_id)
    if current_post.author != current_user:
        abort(403)
    return redirect(url_for('stock.stock_terms_entry_form', post_id=current_post.id))
