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
sys.path.append(r'C:\Users\Angelica Yunshu Li\Documents\HERE\Projects\course_website\website-jinja\templates\py')
import User as u

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

class MainHandler(Handler):
	def get(self):
		#self.write(open('/static/index.html').read())
		self.render('index.html')
	def post(self):
		uid = self.request.get('userid')
		pw = self.request.get('password')
		if 'login' in self.request.POST:
			user = u.login(uid,pw)
			if user:
				#title = "%s's Fall 2016"%user.name
				self.render('main.html',courses=['CS225','cs173'],title = '')
		elif 'signup' in self.request.POST:
			name = self.request.get('name')
			email = self.request.get('email')
			if u.query_id(uid):
				self.write('Username has already been taken.')
			elif u.query_email(email):
				self.write('email taken')
			else:
				user_key = u.signup(name,uid,email,pw)
				if user_key:
					self.write(user_key)
					self.set_ck('key=%s'%user_key)
					self.write('signed up')
		else:
			self.redirect('/')
		




app = webapp2.WSGIApplication([
    ('/', MainHandler)

], debug=True)
