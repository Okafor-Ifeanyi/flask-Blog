from flask import render_template, request, redirect, url_for, flash
# from init app / db = database / bcrypt = encryption / app = Flask var
from Project import db, bcrypt
# gotten from my form file, forms used in the web frame
from Project.user.forms import RegistrationForm, LoginForm, UpdateForm, RequestResetForm, ResetPasswordForm
# gotten from the models file, the main database for storing my data individually
from Project.models import User, Post
# used for the login and logout of a user #downloaded
from flask_login import login_user, current_user, logout_user, login_required
from Project.user.utils import send_request_email, save_picture
from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/register', methods=['GET' ,'POST'])
def register(): 
    # to redirecct the register to home once the user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # getting our info in our froms and storing the as a variable for use
    form = RegistrationForm()
    
    # to validate the submit button if pressed and redirect to the home page
    if form.validate_on_submit():
        # to encrpt password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password= hashed_password)
        db.session.add(user) 
        db.session.commit()
        flash('Your account was successsfully created', 'success' )
        return redirect(url_for('user.login'))
    
    # returns the register with a title name and the forms for registration
    return render_template('register.html', title='Register', form=form)

@user.route('/login', methods=['GET' ,'POST'])
def login():
    # to redirecct the register to home once the user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # getting our info in our froms and storing the as a variable for use
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) :
            login_user(user, remember= form.remember.data)
            # if the next page is bent on the login it takes it here once logged in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Please crosscheck your email address or password', 'danger')   
    # returns the login with a title name and the forms for logining in
    return render_template('login.html', title='Login', form=form) 

@user.route('/logout') 
def logout(): 
    logout_user() 
    return redirect(url_for('main.home')) 

@user.route('/user/<string:username>')
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.data_posted.desc())\
        .paginate(per_page=2, page= page)
    return render_template('user_post.html', posts=posts, user=user)

@user.route('/account', methods= ['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account was successsfully Updated', 'success' )
        return redirect(url_for('user.account'))
    
    elif request.method == 'GET': 
        form.username.data = current_user.username 
        form.email.data = current_user.email 
     
    image_file = url_for('static', filename='profile/' + current_user.image_file) 
    return render_template('account.html', title= 'Account', image_file=image_file, form= form) 

@user.route('/reset_password', methods= ['GET', 'POST']) 
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        send_request_email(user)
        flash('A Request password link has been sent to you on your email', 'info')
        return redirect(url_for('user.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)

@user.route('/reset_password/<token>', methods= ['GET', 'POST']) 
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This token is invalid or expired', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
     # to validate the submit button if pressed and redirect to the home page
    if form.validate_on_submit():
        # to encrpt password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been Successfully Updated', 'success' )
        return redirect(url_for('user.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)