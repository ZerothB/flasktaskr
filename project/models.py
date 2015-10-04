from views import db
import datetime

class Task(db.Model):

	__tablename__="tasks"

	task_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	name = db.Column(db.String, nullable=False)
	due_date = db.Column(db.Date, nullable=False)
	priority = db.Column(db.Integer, nullable=False)
	posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())
	status = db.Column(db.Integer)


	def __init__(self, name, due_date, priority, posted_date, status, user_id):
		self.name = name
		self.due_date = due_date
		self.priority = priority
		self.status = status
		self.user_id = user_id
		self.posted_date = posted_date

	def __repr__(self):
		return '<name {}'.format(self.name)

class User(db.Model):
	"""docstring for User"""

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	tasks = db.relationship('Task', backref='poster')
	name = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=True)
	password = db.Column(db.String, nullable=False)
	role = db.Column(db.String, default='user')

	def __init__(self, name=None, email=None, password=None, role=None):
		self.name = name
		self.email = email
		self.password = password
		self.role = role

	def __repr__(self):
		return '<User {}>'.format(self.name)