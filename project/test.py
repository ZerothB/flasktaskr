import os
import unittest
from views import app, db
from _config import basedir
from models import User
import pdb

TEST_DB = 'test.db'



class AllTests(unittest.TestCase):

	def login(self, name, password):
		return self.app.post('/', data=dict(
			name=name, password=password), follow_redirects=True)

	def register(self, name, email, password, confirm):
		return self.app.post(
			'register/',
			data=dict(name=name, password=password, email=email, confirm=confirm),
			follow_redirects=True
		)

	def logout(self):
		return self.app.get('logout/', follow_redirects=True)

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

	def create_user(self, name, email, password):
		new_user = User(name=name, email=email, password=password)
		db.session.add(new_user)
		db.session.commit()

	def create_task(self):
		return self.app.post('add/', data=dict(
			name='Go to the bank',
			due_date='02/05/2014',
			priority='1',
			posted_date='02/04/2014',
			status='1',
		), follow_redirects=True)

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
		self.create_user('Micheal', 'michael@realpython.com', 'python')
		self.login('Micheal', 'python')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
		self.login('Fletcher', 'python101')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get("complete/1/", follow_redirects=True)
		self.assertNotIn(
			'The task was marked as complete', response.data
		)

		


if __name__ == "__main__":
	unittest.main()

