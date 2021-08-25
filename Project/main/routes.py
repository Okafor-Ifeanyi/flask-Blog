from flask import render_template, request, redirect, url_for, flash, request, abort
from Project.models import Post
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.data_posted.desc()).paginate(per_page=2, page= page)
    return render_template('home.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title = 'About')
