from app import app
from app import db
from app.models import User, Movies, Votes
import datetime

today = datetime.date.today()
weekday = today.weekday()

if (weekday == 4):
	users = db.session.query(User)
	movies = db.session.query(Movies)
	votes = db.session.query(Votes)
	#reset user points
	for u in users:
		u.points = 1
        u.last_vote = None
		print(f"Set {u.username} points: {u.points}")
	#reset movie votes
	for m in movies:
		if m.votes > 0 and m.category == 'cue':
			#m.votes = 0
			m.category = 'archive'
			print(f"Sent {m.movie} into archive")
		elif m.votes == 0 and m.category == 'cue':
			m.votes = 0
			print(f"Reset votes for {m.movie}")
	#reset votes
	for v in votes:
		v.category = 'archive'
		#db.session.delete(v)
	db.session.commit()