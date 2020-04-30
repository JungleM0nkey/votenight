from flask import render_template, flash, redirect, url_for, request, jsonify, abort, g
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import db
from app.forms import LoginForm, RegisterForm, ProfilePasswordForm, ProfileEmailForm
from app.models import User, Movies, Code, Votes
from werkzeug.urls import url_parse
import datetime
from imdb import IMDb
from sqlalchemy import or_, and_
import imageio
import numpy as np

auth = HTTPBasicAuth()

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    #run this if a user is already logged in
    if current_user.is_authenticated:
        return redirect(f'/index/{current_user.username}')
    #run this if a user clicked logged in and filled in all the required fields (u an p)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #if user is invalid or password is wrong
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)
        #if user and password are valid
        login_user(user, remember=form.remember_me.data)
        #security stuff
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', user=user)
        return redirect(next_page)
    error = ''
    return render_template('login.html', form=form, error=error)

@app.route('/index/<user>', methods=['GET','POST'])
@login_required
def index(user):
    #get points for user
    user = User.query.filter_by(username=user).first()
    last_vote = user.last_vote
    points = user.get_points()
    date = get_nextdate()
    session = db.session
    #instance = session.query(Movies) gets all movies, this is no longer needed
    #gets only the movies for this week || Cue
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    #instance = db.session.query(Movies).filter(or_(Movies.date.between(start_week, end_week), Movies.votes > 0))
    instance = db.session.query(Movies).filter(Movies.category == 'cue')
    #gets the other movies || Backlog
    instance_old = db.session.query(Movies).filter(Movies.category == 'backlog')
    instance_archive = db.session.query(Movies).filter(Movies.category == 'archive')
    #instance_old = db.session.query(Movies).filter(and_(~Movies.date.between(start_week, end_week), Movies.votes < 1))
    return render_template('index.html', user=user, points=points, date=date, instance=instance, instance_old=instance_old, last_vote=last_vote,instance_archive=instance_archive)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        #username = username.lower()
        password = form.password.data
        password_confirm = form.password_confirm.data
        invite_code = form.invite_code.data
        existing_code = Code.query.filter_by(code=invite_code).first()
        if password != password_confirm:
            error = 'Passwords do not match'
            return render_template('register.html', form=form, error=error)
        elif not existing_code or existing_code.username != None:
            error = 'Wrong invite code'
            return render_template('register.html', form=form, error=error)
        new_user = User(username=username,points=1)
        new_user.set_password(password)
        existing_code.username = username
        db.session.add(new_user)
        db.session.commit()
        return render_template('register.html', form=form, error='User Created')
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    user = request.form['username']
    user = User.query.filter_by(username=user).first()
    user_movies = db.session.query(Movies).filter(Movies.username == user.username)
    user_votes = db.session.query(Votes).filter(Votes.username == user.username)
    return render_template('profile.html', user=user, user_movies=user_movies, user_votes=user_votes)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/pwchange')
def pwchange():
    return 'test'

def get_nextdate():
    d = datetime.date.today()
    while d.weekday() != 5:
        d += datetime.timedelta(1)
    return d

@app.route('/searchmovie', methods=['GET','POST'])
@login_required
def searchmovie():
    ia = IMDb()
    search_string = request.form['query']
    movies = ia.search_movie(str(search_string))
    movies = [ x['title'] for x in movies ]
    movies = list(set(movies))
    html_list = ''
    for movie in movies:
        html_list += f'\n<div class="search-result"><span>{movie}</span></div>'
    return jsonify({'movies':html_list})

@app.route('/getinfo', methods=['GET','POST'])
@login_required
def getinfo():
    search_string = request.form['query']
    refresh = request.form['refresh']
    existing_movie = Movies.query.filter_by(movie=search_string).first()
    #grab the movie info from the db if it exists
    if existing_movie and refresh == 'false':
        print('Fetching cached movie info')
        movie_name = existing_movie.movie #this will tell the front end to fetch votes for this film
        poster_url = existing_movie.poster
        movie_year = existing_movie.year
        movie_plot = existing_movie.plot
        movie_rating = existing_movie.rating
        movie_genres = existing_movie.genres
        movie_director = existing_movie.director
        movie_imdbpage = existing_movie.imdb_page
    #if not then grab it from imdb 
    elif not existing_movie or refresh == 'true':
        print('Downloading the info from IMDB')
        ia = IMDb()
        movie = ia.search_movie(str(search_string))
        movie_id = movie[0].movieID
        movie_object = ia.get_movie(movie_id)
        movie_imdbpage = f'https://www.imdb.com/title/tt{movie_id}/'
        movie_name = None #this will tell the front end not to fetch votes for this film
        try:
            movie_year = movie_object['year']
        except:
            movie_year = '????'
        try:
            movie_plot = movie_object['plot'][0].split('::')[0]
        except:
            movie_plot = '????'
        try:
            movie_rating = movie_object['rating']
        except:
            movie_rating = '??'
        try: 
            poster_url = movie_object['full-size cover url']
        except:
            poster_url = "/static/images/no-movie-poster.png"
        try:
            movie_genres = movie_object['genres']
            movie_genres = ','.join(movie_genres).replace(',',', ') #this fixes spacing between genres in the string
        except:
            movie_genres = '????'
        try: 
            movie_director = movie_object['director'][0]['name']
        except:
            movie_director = '????'
        #refresh the movie info in the db
        if refresh == 'true':
            print('Saving info into database due to refresh request')
            existing_movie.imdb_page = movie_imdbpage
            existing_movie.year = movie_year
            existing_movie.plot = movie_plot
            existing_movie.rating = movie_rating
            existing_movie.poster = poster_url
            existing_movie.genres = movie_genres #this fixes spacing between genres in the string
            existing_movie.director = movie_director
            db.session.commit()
    #check if the poster is light or dark and let the front end know
    try:
        f = imageio.imread(poster_url, as_gray=True)
        color = img_estim(f, 127)
    except:
        color = 'light'
    return jsonify({'poster':poster_url,'year':movie_year,'plot':movie_plot,'rating':movie_rating,'name':movie_name, 'genres':movie_genres, 'director':movie_director, 'imdbpage':movie_imdbpage, 'color':color})

def img_estim(img, thrshld):
    is_light = np.mean(img) > thrshld
    return 'light' if is_light else 'dark'

@app.route('/addmovie', methods=['GET', 'POST'])
@login_required
def addmovie():
    selected_movie = request.form['selected_movie']
    movie_year = request.form['movie_year']
    movie_rating = request.form['movie_rating']
    movie_plot = request.form['movie_plot']
    movie_poster = request.form['movie_poster']
    movie_genres = request.form['movie_genres']
    current_user = request.form['current_user']
    movie_director = request.form['movie_director']
    existing_movie = Movies.query.filter_by(movie=selected_movie).first()
    #user = User.query.filter_by(username=current_user).first()
    #points = user.points
    #check if movie is already in the database
    if existing_movie:
        return u'Movie already exists', 400
    #check if user has enough points
    #elif points < 1:
    #    return u'Not enough points', 500
    else:
    #grab all the data from IMDB for it and put it into the db
        new_movie = Movies(movie=selected_movie,
                           username=current_user, 
                           votes=0,
                           year=movie_year,
                           rating=movie_rating,
                           plot=movie_plot,
                           poster=movie_poster,
                           genres=movie_genres,
                           director=movie_director,
                           category='backlog'
                           )
        db.session.add(new_movie)
        #user.remove_point() #remove 1 point
        db.session.commit() #commit the db changes
        #points = user.points # grab the new points
        print('Successfuly added movie to database')
        return jsonify({'movie':selected_movie})

@app.route('/vote', methods=['POST'])
@login_required
def vote():
    movie_name = request.form['movie_name']
    vote_point = request.form['vote_point']
    current_user = request.form['current_user']
    movie = Movies.query.filter_by(movie=movie_name).first()
    user = User.query.filter_by(username=current_user).first()
    if user.points > 0 or vote_point == 'minus':
        if vote_point == 'plus':
            user.remove_point()
            user.last_vote = movie_name
            movie.votes = movie.votes + 1
            new_vote = Votes(username=current_user, movie=movie_name, category='current')
            db.session.add(new_vote)
        elif vote_point == 'minus' and movie.votes != 0:
            user.points = user.points + 1
            user.last_vote = None
            movie.votes = movie.votes - 1
            existing_vote = db.session.query(Votes).filter_by(movie=movie_name)
            existing_vote = existing_vote.filter_by(username=current_user).first()
            db.session.delete(existing_vote)
        db.session.commit()
    else:
        return u'Not enough points', 400
    return jsonify({'votes':movie.votes,'points':user.points})

@app.route('/getpoints', methods=['POST'])
@login_required
def getpoints():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    points = user.points
    return jsonify({'points':points})

@app.route('/getvotes', methods=['POST'])
@login_required
def getvotes():
    movie_name = request.form['movie_name']
    votes = Votes.query.filter_by(movie=movie_name, category='current').all()
    votes = [ x.username for x in votes ]
    return jsonify({'votes':votes})

@app.route('/cuemovie', methods=['POST'])
@login_required
def cuemovie():
    movie_name = request.form['movie_name']
    username = request.form['username']
    movie = Movies.query.filter_by(movie=movie_name).first()
    user = User.query.filter_by(username=username).first()
    movie.category = 'cue'
    user.remove_point()
    db.session.commit()
    return jsonify({'category':movie.category, 'username':movie.username, 'points':user.points})

@app.route('/deletemovie', methods=['POST'])
@login_required
def deletemovie():    
    movie_name = request.form['movie_name']
    username = request.form['username']    
    movie = Movies.query.filter_by(movie=movie_name).first()
    #make sure the user is not deleting someone elses movie
    if movie.username == username:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'removed':True})
    else:
        return u'Movie does not belong to user', 400


### API ###

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True

def fetch_movies():
    movies_list = []
    movies = Movies.query.all()
    for movie in movies:
        movie_id = movie.id 
        movie_name = movie.movie
        movie_votes = movie.votes 
        movie_user = movie.username
        movie_date = movie.date
        movie_object = {'id':movie_id,
                        'name':movie_name,
                        'votes':movie_votes,
                        'user':movie_user,
                        'date':movie_date}
        movies_list.append(movie_object)
    return movies_list

def make_public_movie(movie):
    new_movie = {}
    for field in movie:
        if field == 'id':
            new_movie['uri'] = url_for('get_movie', movie_id=movie['id'], _external=True)
        else:
            new_movie[field] = movie[field]
    return new_movie

@app.route('/api/1.0/movies', methods=['GET'])
@auth.login_required
def get_movies():
    movies_list = fetch_movies()
    return jsonify({ 'movies': [make_public_movie(movie) for movie in movies_list] })

@app.route('/api/1.0/movies/<int:movie_id>', methods=['GET'])
@auth.login_required
def get_movie(movie_id):
    movies_list = fetch_movies()
    movie = [ x for x in movies_list if x['id'] == movie_id ]
    if len(movie) == 0:
        abort(404)
    return jsonify({'movie':movie[0]})