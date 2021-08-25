# web frame and properties
from flask import render_template, request, redirect, url_for, flash, request, abort
# from init app / db = database / bcrypt = encryption of password / app = Flask var
from Project import db
# gotten from my form file, forms used in the web frame
from Project.posts.forms import PostForm
# gotten from the models file, the main database for storing my data individually
from Project.models import Post
# used for the login and logout of a user #downloaded
from flask_login import current_user, login_required
from flask import Blueprint

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods= ['GET', 'POST']) 
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Post( title= form.title.data, content= form.content.data, author= current_user)
        db.session.add(posts)
        db.session.commit()
        flash('Your message was successfully posted', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New post',
     form= form, legend= 'New Post') 

@posts.route('/post/<int:post_id>', methods= ['GET', 'POST']) 
@login_required
def Posts(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('Post.html', title='post.title', post=post)   

@posts.route('/post/<int:post_id>/update', methods= ['GET', 'POST']) 
@login_required
def Update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post was successfully Updated', 'success')
        return redirect(url_for('posts.Posts', post_id= post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('Create_post.html', title='Update Post',
     form= form, legend= 'Update Post') 


@posts.route('/post/<int:post_id>/delete', methods= ['POST']) 
@login_required
def Delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'Success')
    return redirect(url_for('main.home'))

