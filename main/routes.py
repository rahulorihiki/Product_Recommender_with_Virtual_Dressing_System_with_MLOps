from functools import wraps
from flask import render_template,url_for,request,redirect,flash,session
from main import app , connection1 , connection2
import json
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length , ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
from numpy.linalg import norm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.neighbors import NearestNeighbors
from flask_paginate import Pagination
from tensorflow.keras.models import load_model
from myFashionRecommender.config.configuration import ConfigurationManager
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import gdown

app_config = ConfigurationManager().get_app_config()

gdown.download(app_config.extracted_features_path, 'downloaded_artifacts/features.pkl', quiet=False)
gdown.download(app_config.filenames_path, 'downloaded_artifacts/filenames.pkl', quiet=False)
gdown.download(app_config.model_path, 'downloaded_artifacts/model.h5', quiet=False)

feature_list = np.array(pickle.load(open('downloaded_artifacts/features.pkl','rb')))
filenames = pickle.load(open('downloaded_artifacts/filenames.pkl','rb'))

# Load the model
model = load_model('downloaded_artifacts/model.h5')

# Read the excel file that contains image id and the corresponding image url
image_df = pd.read_csv(app_config.image_df_path)

# Fit the Nearest Neighbors model
neighbors = NearestNeighbors(n_neighbors=app_config.knn_neighbors,algorithm=app_config.knn_algorithm,metric=app_config.knn_metric)
neighbors.fit(feature_list)

# Fetching data from the database
cursor1 = connection1.cursor()
cursor1.execute("SELECT DISTINCT articleType FROM 'products' ")
distinct_fashion = cursor1.fetchall()

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if session.get("logged_in"):
            # User is logged in, allow access to the protected route
            return view_func(*args, **kwargs)
        else:
            # User is not logged in, redirect to the login page
            next_url = request.url
            return redirect(url_for('login', next=next_url))
    return wrapped_view

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

    def validate_username(self, username):
        query = "SELECT * FROM user123 WHERE username = ?"
        cursor = connection2.cursor()
        cursor.execute(query, (username.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError('That username is taken. Please choose a new one')

    def validate_email(self, email):
        query = "SELECT * FROM user123 WHERE email = ?"
        cursor = connection2.cursor()
        cursor.execute(query, (email.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError('That email is taken. Please choose a new one')

@app.route("/")
def contact():
    return render_template("index.html")

@app.route("/search/<data>" , methods = ["POST"])
def search(data):
    fashion_list = []
    for elements in distinct_fashion:
        try:
            (elements[0].lower()).index(data)
        except ValueError:
            pass  # do nothing!
        else:
            fashion_list.append(elements[0])

    lengthss = len(fashion_list)
    fashion_string = str(lengthss)
    for i in range(lengthss - 1):
        fashion_string += '`'+fashion_list[i]
    if(lengthss == 1):
        fashion_string = str(fashion_list[0])
    
    return fashion_string
    

@app.route("/search-result/<a>", methods=["POST", "GET"])
def search_result(a):
    page = request.args.get('page', 1, type=int)
    cursor = connection1.cursor()
    if a == 'Tshirts':
        query = "SELECT * FROM products WHERE articleType = ? AND gender = 'Men'"
        cursor.execute(query, (a,))
    else:
        query = "SELECT * FROM products WHERE articleType = ?"
        cursor.execute(query, (a,))
    result = cursor.fetchall()
    
    # Perform pagination manually if needed
    per_page = 9
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    pro = result[start_idx:end_idx]
    final_pro = []
    for product in pro:
        image_name = f'{product[1]}.jpg'
        image_url = image_df.loc[image_df['filename'] == image_name]['link'].values[0]
        final_pro.append((product[1],product[-1],image_url))

    pagination = Pagination(page=page, per_page=per_page, total=len(result),css_framework='bootstrap4')

    return render_template("shop.html", final_pro=final_pro, pagination=pagination)


@app.route("/search-result_subcategory/<a>")
def search_result_subcategory(a):
    page = request.args.get('page', 1, type=int)
    cursor = connection1.cursor()
    query = f"SELECT * FROM products WHERE subCategory = ?"
    cursor.execute(query, (a,))
    result = cursor.fetchall()
    
    # Perform pagination manually if needed
    per_page = 9
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    pro = result[start_idx:end_idx]
    final_pro = []
    for product in pro:
        image_name = f'{product[1]}.jpg'
        image_url = image_df.loc[image_df['filename'] == image_name]['link'].values[0]
        final_pro.append((product[1],product[-1],image_url))

    pagination = Pagination(page=page, per_page=per_page, total=len(result),css_framework='bootstrap4')

    return render_template("shop.html", final_pro=final_pro,pagination = pagination)


@app.route("/search-result_mastercategory/<a>")
def search_result_mastercategory(a):
    page = request.args.get('page', 1, type=int)
    cursor = connection1.cursor()
    query = "SELECT * FROM products WHERE masterCategory = ?"
    cursor.execute(query, (a,))
    result = cursor.fetchall()
    per_page = 9
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    pro = result[start_idx:end_idx]
    final_pro = []
    for product in pro:
        image_name = f'{product[1]}.jpg'
        image_url = image_df.loc[image_df['filename'] == image_name]['link'].values[0]
        final_pro.append((product[1],product[-1],image_url))

    pagination = Pagination(page=page, per_page=per_page, total=len(result),css_framework='bootstrap4')

    return render_template("shop.html", final_pro=final_pro,pagination=pagination)


def recommend(id):
    image_name = f'{id}.jpg'
    image_url = image_df.loc[image_df['filename'] == image_name]['link'].values[0]
    response = requests.get(image_url)
    response.raise_for_status() # Ensure the request was successful
    img = Image.open(BytesIO(response.content)) # Open the image from the response
    # Convert the image to the desired format and resize it
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)

    distances,indices = neighbors.kneighbors([normalized_result])

    ind = []
    for file in indices[0][1:6]:
        ind.append(filenames[file][32:])

    return ind



@app.route("/product-detail")
@login_required
def product_detail():
    id = request.args.get('id' , type = int)
    # id = 39386
    cursor1 = connection1.cursor()
    cursor1.execute("SELECT * FROM 'products' where id = ? " , (str(id),) )
    # fashion_d = cursor1.fetchall()
    with open("main/static/fashion-dataset/styles/" +str(id)+".json") as f:
        data = json.load(f)
    valval0 = data["data"]["styleImages"]["default"]["imageURL"]
    # For the Back image perspective
    try:
        data["data"]["styleImages"]["back"]["imageURL"]
    except KeyError:
        valval1 = "not_available"
    else:
        valval1 = data["data"]["styleImages"]["back"]["imageURL"]
    #For the left image perspective
    try:
        data["data"]["styleImages"]["left"]["imageURL"]
    except KeyError:
        valval2 = "not_available"
    else:
        valval2 = data["data"]["styleImages"]["left"]["imageURL"]
    
    #For the right image perspective
    try:
        data["data"]["styleImages"]["right"]["imageURL"]
    except KeyError:
        valval3 = "not_available"
    else:
        valval3 = data["data"]["styleImages"]["right"]["imageURL"]


    data_obj = {
        "id" : data["data"]["id"],
        "displayName" : data["data"]["productDisplayName"],
        "price" : data["data"]["price"],
        "brandName" : data["data"]["brandName"],
        "ageGroup" : data["data"]["ageGroup"],
        "gender" : data["data"]["gender"],
        "color" : data["data"]["baseColour"],
        "season" : data["data"]["season"],
        "year" : data["data"]["year"],
        "usage" : data["data"]["usage"],
        "productAttribute" : data["data"]["articleAttributes"],
        "brandInfo" : data["data"]["brandUserProfile"],
        "default_img_url" : valval0,
        "back_img_url" : valval1,
        "left_img_url" : valval2,
        "right_img_url" : valval3,
    }
    len1 = len(data_obj['productAttribute'])
    len2 = len(data_obj['brandInfo'])

    #Doing the recommendation part
    ind = recommend(data_obj['id'])
    images = []
    for i in ind:
        image_name = i
        image_url = image_df.loc[image_df['filename'] == image_name]['link'].values[0]
        images.append([i,image_url])
    return render_template("detail.html" , data_obj = data_obj , len1 = len1 , len2 = len2 , images = images)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        username = form.username.data
        email = form.email.data
        password = hashed_password
        query = "INSERT INTO user123 (username, email, password) VALUES (?, ?, ?)"
        cursor = connection2.cursor()
        cursor.execute(query, (username, email, password))
        connection2.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_url = request.form.get("next")
    if session.get("logged_in"):
         return redirect(url_for('contact'))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        query = "SELECT * FROM user123 WHERE username = ?"
        cursor = connection2.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[3], password):
            # Assuming the password hash is stored at index 2 in the user123 table
            flash(f"Welcome {username}! You have successfully logged in to our website.", 'success')
            session["logged_in"] = True
            session["user_id"] = user[0]
            session["username"] = user[1]
            if next_url:
                    return redirect(next_url)
            # Login logic and redirection
            return redirect(url_for('contact'))

        flash("You have entered wrong username or password, please try again.", "danger")
        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    # logout_user()
    session["logged_in"] = False
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('contact'))


# Routes for custom error pages

@app.errorhandler(404)
def error_404(error):
    return render_template("404.html") , 404

@app.errorhandler(403)
def error_403(error):
    return render_template("403.html") , 403

@app.errorhandler(500)
def error_500(error):
    return render_template("500.html") , 500


