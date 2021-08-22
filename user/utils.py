# for path of doc's anywhere in your os
import os 
# Making unique digits
import secrets
# for resizing images
from PIL import Image
# web frame and properties
from flask import url_for, current_app
# from init app / db = database / bcrypt = encryption of password / app = Flask var
from Project import mail
# for sending message to the users email
from flask_mail import Message

def save_picture(form_picture):
    # Gets 8 unique numbers and saves it with var random_hex
    random_hex = secrets.token_hex(8)
    # gets path and splits the name from the extension
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

    # Resize image
    # output_size = (100,100)
    i = Image.open(form_picture)
    # i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_request_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='zeusifeanyi058@gmail.com', recipients=[user.email])
    msg.body = f''' Welcome to your reset password request. Really hope its you tho. Click on the link to continue...
{url_for('user.reset_token', token=token, _external=True)}
    '''
    mail.send(msg) 

