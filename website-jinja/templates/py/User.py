from google.appengine.ext import ndb
import validation as v

class User(ndb.Model):
	name = ndb.StringProperty(required=True)
	userid = ndb.KeyProperty(required=True)
	email = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	major = ndb.StringProperty()
	joinded_time = ndb.DateTimeProperty(auto_now_add=True)


def query_id(id):
	qry = User.query().filter(User.userid == id)
	return qry.fetch()

def query_email(em):
	qry = User.query().filter(User.email == em)
	return qry.fetch()

def login(id,pw):
	return True
	user = query_id(id)
	if v.pw_hash(id,pw) == user.password:
		return user

def signup(name,id,email,pw):
	user = User(name=name,userid=id,email=email,password=pw)
	user_key=user.put()
	return user_key

def gpa_calc():
	pass