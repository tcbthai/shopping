from . import admin
from flask import redirect, render_template, flash, url_for, request, g
from flask_login import login_required
from .forms import CategoriesCreate, PostForm
from app.models_sqldb import Category, Product, User
from app import db


# from app.decorators import admin_required, mod_required

# Categories Dashboard
@admin.route('/admin/categories/create', methods=['GET', 'POST'])
@login_required
def admin_categories_create():
    form = CategoriesCreate()
    if form.validate_on_submit() and request.method == 'POST':
        category = Category(name=form.new_category.data)
        db.session.add(category)
        db.session.commit()
        flash('Saved')
        return redirect(url_for('.admin_categories'))
    return render_template('auto_form.html', form=form)


@admin.route('/admin/categories')
@login_required
def admin_categories():
    categories = Category.query.all()
    head_list = ['Name']
    return render_template('admin/admin_dashboard.html', categories=categories, head_list=head_list)


@admin.route('/admin/categories/<category_id>/delete')
@login_required
def admin_cat_delete(category_id):
    category = Category.query.get(category_id).first()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('.admin_categories'))


@admin.route('/admin/categories/<category_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_cat_edit(category_id):
    category = Category.query.get(category_id)
    form = CategoriesCreate()
    if request.method == 'POST' and form.validate_on_submit():
        category.name = form.new_category.data
        category.save()
        flash('Saved')
        return redirect(url_for('.admin_categories'))
    form.new_category.data = category.name
    return render_template('auto_form.html', form=form)


# Posts Dashboard
@admin.route('/admin/products/create', methods=['GET', 'POST'])
@login_required
def product_create():
    form = PostForm()
    category_list = g.category_list
    my_cat = []
    for i in category_list:
        my_cat.append((i.name, i.name.title()))
    form.category.choices = my_cat
    if form.validate_on_submit() and request.method == 'POST':
        product_category = Category.query.filter_by(name=form.category.data).first_or_404()
        product = Product(image=form.image.data,
                          description=form.description.data,
                          category=product_category,
                          product_code=form.code.data,
                          name=form.name.data,
                          price=form.price.data,
                          detail=form.detail.data,
                          stock=form.stock.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.products_view'))
    return render_template('auto_form.html',
                           form=form,
                           category_list=category_list,
                           )


@admin.route('/admin')
@admin.route('/admin/products')
@login_required
def products_view():
    products = Product.query.all()
    head_list = ['Name', 'Price', 'Stock', 'Category']
    return render_template('admin/admin_dashboard.html', products=products, head_list=head_list)


@admin.route('/admin/products/<product_id>/delete')
@login_required
def products_delete(product_id):
    post = Product.query.get(product_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.products_view'))


@admin.route('/admin/products/<product_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_posts_edit(product_id):
    form = PostForm()
    category_list = g.category_list
    my_cat = []
    for i in category_list:
        my_cat.append((i.name, i.name.title()))
    form.category.choices = my_cat
    product = Product.query.get(product_id)
    if form.validate_on_submit() and request.method == 'POST':
        product_category = Category.query.filter_by(name=form.category.data).first_or_404()
        product.image = form.image.data
        product.description = form.description.data
        product.category = product_category
        product.product_code = form.code.data
        product.name = form.name.data
        product.price = form.price.data
        product.detail = form.detail.data
        product.stock = form.stock.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.products_view'))
    form.image.data = product.image
    form.description.data = product.description
    form.code.data = product.product_code
    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.detail.data = product.detail
    form.category.data = product.category.name
    return render_template('auto_form.html', form=form, category_list=category_list)
