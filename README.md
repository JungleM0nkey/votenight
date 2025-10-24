### Flask web application for voting on Movies & TV Shows
![alt text](https://i.imgur.com/p17S3jI.png "votenight.ca preview")

Setup:
1. pip install -r requirements.txt
2. run setup.py, this will rename sample.db to app.db
3. Run database migration: `flask db upgrade`
4. run the command: flask run
5. Navigate to http://127.0.0.1:5000/ U: admin P: moose

Discord SSO Setup (Optional):
1. Go to https://discord.com/developers/applications
2. Create a new application or select an existing one
3. Navigate to OAuth2 settings
4. Add redirect URL: `http://localhost:8000/auth/discord/callback` (or your production URL)
5. Copy your Client ID and Client Secret
6. Set environment variables:
   ```
   export DISCORD_CLIENT_ID='your-client-id'
   export DISCORD_CLIENT_SECRET='your-client-secret'
   export DISCORD_REDIRECT_URI='http://localhost:8000/auth/discord/callback'
   ```
7. Users can now login with Discord on the login page


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

