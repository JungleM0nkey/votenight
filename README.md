### Flask web application for voting on Movies & TV Shows
![alt text](https://i.imgur.com/p17S3jI.png "votenight.ca preview")

Setup:
1. pip install -r requirements.txt
2. run setup.py, this will rename sample.db to app.db
3. run the command: flask run
4. Navigate to http://127.0.0.1:5000/ U: admin P: moose


API Usage (Requires authentication):
1. To get movies send a GET request to <http://127.0.0.1:5000/api/1.0/movies>

2. To get a single movie send a GET request to <http://127.0.0.1:5000/api/1.0/movies/<movie_id>>

3. To vote on a film send a POST request to <http://127.0.0.1:5000/api/1.0/movies/vote> with the following JSON data: 
```"Movie":"your-movie-name","Action":"up/down"```

4. To search and add a movie to the viewing backlog send a POST request to <http://127.0.0.1:5000/api/1.0/movies/add> with the following JSON data: 
```"Movie":"your-movie-name"```

5. To delete a movie send a POST request to <http://127.0.0.1:5000/api/1.0/movies/delete> with the following JSON data:
```"Movie":"your-movie-name"```

6. To move a movie from the backlog to the que send a POST request to <http://127.0.0.1:5000/api/1.0/movies/que> with the following JSON data:
```"Movie":"your-movie-name"```

