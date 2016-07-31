#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import sys
#sys.path.append(r'C:\Users\Angelica Yunshu Li\Documents\HERE\Projects\course_website\website-jinja\templates\py')
from User import *
import json

FOLDERNAME = "templates" 	# only for self.render(template)   e.g. html files


template_dir = os.path.join(os.path.dirname(__file__), FOLDERNAME)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def set_ck(self,cookie):
		self.response.headers.add_header('Set-Cookie',cookie)

	def get_ck(self,cookie):
		return self.request.cookies.get(cookie)

	def load(self,page,user,active='home'):
		courseinfo = (json.loads(user.courseinfo) if user.courseinfo else {})
		courses=(json.loads(user.courses) if user.courses else [])
		name=user.name
		self.render(page,user=user,name=name,courses=courses,courseinfo=courseinfo,active=active)

class MainHandler(Handler):
	def get(self):
		self.render('signup.html')
	def post(self):
		uid = self.request.get('userid')
		pw = self.request.get('password')
		if 'login' in self.request.POST:
			user = login(uid,pw)
			if user:
				ck = text_hash(user.userid)
				self.set_ck(str("id=%s"%ck))
				#title = "%s's Fall 2016"%user.name
				self.redirect('/%s'%uid)
			else:
				self.render('signup.html',loginerror='Invalid username and/or password.',loginactive=True)
		elif 'signup' in self.request.POST:
			name = self.request.get('name').capitalize()
			email = self.request.get('email')
			if query_id(uid):
				self.render('signup.html',signuperror='This username has already been taken.')
			elif query_email(email):
				self.render('signup.html',signuperror='This email has already been registered.')
			else:
				user_key = signup(name,uid,email,pw)
				if user_key:
					user = user_key.get()
					ck = text_hash(user.userid)
					self.set_ck(str("id=%s"%ck))
					userurl = '/'+user.userid
					self.redirect('/%s'%uid)
		else:
			self.write("???")

class UserHandler(Handler):
	def get(self,userid):
		user = query_id(userid)[0]
		if user.courses:
			self.load('main.html', user,active='home')
		else:
			self.redirect('/%s/settings'%userid)

class CourseHandler(Handler):
	def get(self,userid,courseid):
		user = query_id(userid)[0]
		if user.courses:
			self.load('main.html', user,active=courseid)
		else:
			self.redirect('/%s/settings'%userid)


class SettingsHandler(Handler):
	def get(self,userid):
		user = query_id(userid)[0]
		self.load('setup.html',user= user)
	def post(self,userid):
		user = query_id(userid)[0]
		if 'setup' in self.request.POST:		# new user (first time setup)
			# update user.courses
			user.courses = json.dumps(self.request.get('course-list').split())
			# update user.courseinfo
			courseinfo = {}
			for course in user.courses:
				courseinfo[course] = {}
				courseinfo[course] = {}
			user.courseinfo = json.dumps(courseinfo)
			# commit updated user
			user.put()
			# reload page
			self.load('setup.html', user = user)
		elif 'update' in self.request.POST:		# not first time
			# @TODO: add update function
			self.write("update request")

		else:
			self.write("nothing?")
			



app = webapp2.WSGIApplication([
    ('/', MainHandler), webapp2.Route('/<userid>',UserHandler),webapp2.Route('/<userid>/settings',SettingsHandler),webapp2.Route('/<userid>/<courseid>',CourseHandler)

], debug=True)
