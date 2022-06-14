from flask import flash, redirect, render_template, url_for, request
from app import app, admin, db, bcrypt
from app.models import Product, User, Cart
from app.form import UserRegistration, LoginForm, Buy, Cash, UpdateAccount
from flask_login import login_required, login_user, current_user, logout_user
from app.utils import MyModelView



admin.add_view(MyModelView(Product, db.session))



@app.route('/')
def home():
	goods = Product.query.all()
	return render_template('home.html', title='Products', goods=goods)



@app.route('/register', methods=['GET', 'POST'])
def reg():
	form = UserRegistration()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user = User(first_name =form.first_name.data,
			        email=form.email.data, address=form.address.data, password = hashed_password, seller = form.seller.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('reg.html', title='Register', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		user = User.query.filter_by(email= form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user=user, remember=form.remember_me.data)
			flash('Good job', 'success')
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		flash('Access Denied', "danger")
	return render_template('login.html',title='Login', form=form)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	flash("Get out mutherfucker")
	return redirect(url_for("home"))




@app.route('/categories', methods=['GET', 'POST'])
def categories():
	goods = Product.query.with_entities(Product.category).distinct()
	return render_template('product.html', title='Categories', goods=goods)



@app.route('/singleproduct/<int:product_id>', methods=['GET', 'POST'])
def single_product(product_id):
	single = Product.query.filter_by(id=product_id).first()
	form = Buy()
	if form.validate_on_submit():
		red = form.quantity.data
		return redirect(url_for('buy', id=single.id ,red=red))
	image_file = url_for('static', filename='profile_pic/' + single.product_pic)
	return render_template('buy.html', title='Categories', post=single, pic=image_file, form=form)

#  render template is temporary. route to serve as a button
@app.route('/buy/<int:id>/<int:red>', methods=['GET', 'POST'])
@login_required
def buy(id, red):
	post = Product.query.filter_by(id=id).first()
	form = red
	print(form)
	if post.quantity > 0:
		if current_user.cash >= post.price:
			if post.quantity >= form and form > 0:
				cart = Cart(user_id=current_user.id, product_id=post.id, quantity=form)
				db.session.add(cart)
				db.session.commit()
				flash('Added to cart')
				return redirect(url_for('cart'))
			else:
				flash('Not Enough stock')
		else:
				flash('Not Enough cash')
	else:
		flash("Out in stock")
	return redirect(url_for('home'))




# add cash form to individual product page
@app.route('/cash/<int:id>', methods=['GET', 'POST'])
@login_required
def cash(id):
	user = User.query.get_or_404(id)
	form = Cash()
	if form.validate_on_submit():
		user.cash += form.cash.data
		db.session.commit()
		flash('Cha ching')
		return redirect(url_for('user', id=current_user.id))
	return render_template('cash.html', title='Buy Product', form=form, post=user)



@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
	cart = Cart.query.filter_by(user_id=current_user.id).all()
	r = db.session.query(Cart.quantity, Product.name, Product.price, Product.product_pic).filter(Cart.user_id == current_user.id ,Cart.product_id == Product.id).all()
	return render_template('cart.html', title='Cart', cart=cart, r=r)



@app.route('/singlecat/<string:category>', methods=['GET', 'POST'])
def single_cat(category):
	single = Product.query.filter(Product.category.like(category)).all()
	return render_template('single_category.html', title='Categories', goods=single)


@app.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user(id):
	user = User.query.get_or_404(id)
	return render_template('dashboard.html', title='Dashboard', user=user)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_account(id):
	user = User.query.get_or_404(id)
	form = UpdateAccount()
	if form.validate_on_submit():
		user.email = form.email.data
		user.first_name = form.first_name.data
		user.address = form.address.data
		if form.seller.data == True:
			user.seller = form.seller.data
		db.session.commit()
		flash('Updated')
		return redirect(url_for('user', id=current_user.id))
	elif request.method == 'GET':
		form.email.data = current_user.email
		form.first_name.data = current_user.first_name
		form.address.data = current_user.address
	return render_template('update.html', title='Update Account', user=user, form=form)

# To later add a checkout route and deduct the quantity on puchase