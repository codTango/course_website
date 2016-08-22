from google.appengine.ext import ndb

class Course(ndb.Model):
	id = ndb.StringProperty(required=True)
	subject = ndb.StringProperty()
	number = ndb.IntegerProperty()
	website = ndb.JsonProperty()	#{"www.coursesite.com":3,"www.subsite.com":1} records numbers of time people choose it
	homework = ndb.JsonProperty()
	calendar = ndb.JsonProperty()
	grades = ndb.JsonProperty()
	syllabus = ndb.JsonProperty()

class User(ndb.Model):
	name = ndb.StringProperty(required=True)
	userid = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	schedule = ndb.BlobProperty()
	courseinfo = ndb.JsonProperty()	# {course1:{"Course Website":"www.xxx.com","Homework":"hw.com"}, course2:{...}}
	joined_time = ndb.DateTimeProperty(auto_now_add=True)
	rememberme = ndb.IntegerProperty()

########### validation #####################
import hashlib
import random
from string import letters
SECRET = "kiwiNinja"

def make_salt():
	return ''.join(random.choice(letters) for _ in range(5))

def pw_hash(id,pw,salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(id+pw+salt).hexdigest()
	return '%s|%s'%(h,salt)

def valid_pw(id,pw,HASH):
	salt = HASH.split('|')[1]
	if pw_hash(id,pw,salt) == HASH:
		return True


def text_hash(text):
	h = hashlib.sha256(text+SECRET).hexdigest()
	return '%s|%s'%(text,h)

def valid_id(HASH):
	id = HASH.split('|')[0]
	if text_hash(id) == HASH:
		return id

########### validation #####################



########## login/signup #####################
def query_id(uid):
	try:
		qry = User.query().filter(User.userid == uid)
		return qry.fetch()[0]
	except:
		return None

def query_email(em):
	qry = User.query().filter(User.email == em)
	return qry.fetch()

def query_key(key):
	qry = User.query().filter(User.key == key)
	return qry.fetch()

def login(id,pw):
	user = query_id(id)
	if user and valid_pw(id,pw,user.password):
		return user

def signup(name,id,email,pw):
	pw = pw_hash(id,pw)
	user = User(name=name,userid=id,email=email,password=pw)
	user_key=user.put()
	return user_key

########## login/signup #####################

########## course fucntions ##################
def course_info_converter(text):
	for line in text.splitlines():
		try:
			lst = line.split('\t')
			crn = int(lst[0])
			subject,number,section = lst[1].split()
			name = lst[2]
			prof = lst[-1]
			credit = int(lst[4][0])
		except:
			pass

def query_courseid(id):
	qry = Course.query().filter(Course.id == id)
	return qry.fetch()[0]
########## course fucntions ##################


########## extra features ##################
def gpa_calc():
	pass

########## extra features ##################





