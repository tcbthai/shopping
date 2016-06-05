from flask import render_template, redirect, url_for, g, current_app, request, session
from . import main
from app.models_sqldb import User, Category, Product
from forms import Contact_Form
from flask_login import current_user
from app.email import send_contact_mail
from cart import Cart

cart = Cart(session)


@main.route('/')
@main.route('/index')
@main.route('/index/page<int:page>')
def index(page=1):
    pagination = Product.query.order_by(Product.created_date.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)

    return render_template('index.html', pagination=pagination)


@main.route('/categories/<int:id>')
@main.route('/categories/<int:id>/page<int:page>')
def category(id, page=1):
    pagination = Product.query.join(Product.category).filter(Category.id == id).paginate(page, 3, False)
    return render_template('index.html', pagination=pagination, cat=True)


@main.route('/products/<product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        cart.add_to_cart(request, product_id)
        return redirect(url_for('.product_detail', product_id=product_id))
    return render_template('detail.html', product=product)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Contact_Form()
    if current_user.is_authenticated:
        form.name.data = current_user.nickname
    if form.validate_on_submit():
        send_contact_mail(form.email.data, form.content.data, form.name.data + '<chuvi0902@gmail.com>')
        return redirect(url_for('main.index'))
    return render_template('auto_form.html', form=form, header="Contact")
