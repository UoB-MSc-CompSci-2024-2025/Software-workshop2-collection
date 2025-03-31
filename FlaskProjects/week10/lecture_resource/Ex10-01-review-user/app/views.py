from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User, Address, Product, Review
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, RegisterForm, AddressForm, ReviewForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io

@app.route("/")
def home():
    return render_template('home.html', title="Home")


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    addr_form=AddressForm()
    choose_form = ChooseForm()
    if addr_form.validate_on_submit():
        phone = addr_form.phone.data.strip()
        if phone == '':
            phone = None
        if addr_form.edit.data == '-1':
            addr = Address(tag=addr_form.tag.data, address = addr_form.address.data, phone = phone)
            current_user.addresses.append(addr)
        else:
            addr = db.session.get(Address, int(addr_form.edit.data))
            addr.tag = addr_form.tag.data
            addr.address = addr_form.address.data
            addr.phone = phone
        db.session.commit()
        # The redirect has the effect of a clean restart of the page with a clear form
        return redirect(url_for('account'))
    return render_template('account.html', title="Account", form=addr_form, choose_form=choose_form)

@app.route("/edit_addr", methods=['POST'])
def edit_addr():
    choose_form = ChooseForm()
    if choose_form.validate_on_submit():
        addr = db.session.get(Address, choose_form.choice.data)
        addr_form = AddressForm(edit=addr.id, tag=addr.tag, address=addr.address, phone=addr.phone)
        return render_template('account.html', title="Account", form=addr_form, choose_form=choose_form)
    return redirect(url_for('account'))


@app.route("/delete_addr", methods=['POST'])
def delete_addr():
    form = ChooseForm()
    if form.validate_on_submit():
        addr = db.session.get(Address, form.choice.data)
        db.session.delete(addr)
        db.session.commit()
    return redirect(url_for('account'))


@app.route("/admin")
@login_required
def admin():
    if current_user.role != "Admin":
        return redirect(url_for('home'))
    form = ChooseForm()
    q = db.select(User)
    user_lst = db.session.scalars(q)
    return render_template('admin.html', title="Admin", user_lst=user_lst, form=form)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        q = db.select(User).where((User.role == "Admin") & (User.id != u.id))
        first = db.session.scalars(q).first()
        if not first:
            flash("You can't delete your own account if there are no other admin users!", "danger")
        elif u.id == current_user.id:
            logout_user()
            db.session.delete(u)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            db.session.delete(u)
            db.session.commit()
    return redirect(url_for('admin'))

@app.route('/toggle_user_role', methods=['POST'])
def toggle_user_role():
    form = ChooseForm()
    if form.validate_on_submit():
        u = db.session.get(User, int(form.choice.data))
        q = db.select(User).where((User.role == "Admin") & (User.id != u.id))
        first = db.session.scalars(q).first()
        if not first:
            flash("You can't drop your admin role if there are no other admin users!", "danger")
        elif u.id == current_user.id:
                logout_user()
                u.role = "Normal"
                db.session.commit()
                return redirect(url_for('home'))
        else:
            u.role = "Normal" if u.role == "Admin" else "Admin"
            db.session.commit()
    return redirect(url_for('admin'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)

@app.route('/change_pw', methods=['GET', 'POST'])
@fresh_login_required
def change_pw():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed successfully', 'success')
        return redirect(url_for('home'))
    return render_template('generic_form.html', title='Change Password', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('generic_form.html', title='Register', form=form)

@app.route("/products")
def products():
    q = db.select(Product)
    products = db.session.scalars(q)
    # return redirect(url_for('product', id=int(form.choice.data)))
    return render_template('products.html', title="Products", products=products)

@app.route("/product/<int:id>", methods=['GET', 'POST'])
def product(id):
    product = db.session.get(Product, id)
    if not product:
        return redirect(url_for('products'))
    form = ReviewForm()
    if current_user.is_authenticated and form.validate_on_submit():
        text = form.text.data.strip()
        text = None if text == '' else text
        review = Review(user=current_user, stars=int(form.stars.data), text=text)
        product.reviews.append(review)
        try:
            db.session.commit()
        except sa.exc.IntegrityError as err:
            flash('Error: you already have a review for this product', 'danger')
            app.logger.warning(f'IntegrityError: {err=}')
            db.session.rollback()
        return redirect(url_for('product', id=id))
    q = db.select(sa.func.avg(Review.stars)).where(Review.product == product)
    avg_stars = db.session.scalar(q)
    return render_template('product.html', title='Product', form=form, product=product, avg_stars=avg_stars)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500