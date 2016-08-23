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
# sys.path.append(r'C:\Users\Angelica Yunshu Li\Documents\HERE\Projects\course_website\website-jinja\templates\py')
from User import *
import json
from webapp2_extras import routes
from random import getrandbits as bits
import time
import datetime
import logging

FOLDERNAME = "templates"  # only for self.render(template)   e.g. html files

template_dir = os.path.join(os.path.dirname(__file__), FOLDERNAME)
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)




class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_ck(self, name,value,expires=None):
        self.response.set_cookie(name, value, expires=expires,path='/')

    def get_ck(self, cookie):
        return self.request.cookies.get(cookie)

    def rememberme(self,user,temp=True):
        ck = bits(11)
        user.rememberme = ck
        user.put()
        if temp:
            exp = None
        else:
            exp = (datetime.datetime.now() + datetime.timedelta(weeks=50))
        self.set_ck("rememberme",str(ck),expires=exp)

    def load(self, page, user, active='home'):
        courses = (json.loads(user.courseinfo) if user.courseinfo else {})
        urls = filter(lambda tup: tup[0]==active, courses)[0][1]
        name = user.name
        self.render(page, user=user, name=name, courses=courses, active=active,urls=urls)


class MainHandler(Handler):
    def get(self):
        self.render('signup.html')

    def post(self):
        uid = self.request.get('userid')
        pw = self.request.get('password')
        if 'login' in self.request.POST:
            user = login(uid, pw)
            if user:
                if self.request.get("rememberme"): 
                    self.rememberme(user,temp=False)
                else:
                    self.rememberme(user)
                time.sleep(1)
                self.redirect("/%s/settings"%uid)
            else:
                self.render('signup.html', loginerror='Invalid username and/or password.', page="login")
        elif 'signup' in self.request.POST:
            name = self.request.get('name').capitalize()
            email = self.request.get('email')
            if query_id(uid):
                self.render('signup.html', signuperror='This username has already been taken.')
            elif query_email(email):
                self.render('signup.html', signuperror='This email has already been registered.')
            else:
                user_key = signup(name, uid, email, pw)
                if user_key:
                    self.rememberme(user_key.get())
                    self.redirect('/%s' % uid)
                else:
                    self.write("signup failed")
        else:
            self.write("???")


class UserHandler(Handler):
    def get(self, userid):
        user = query_id(userid)
        if not user:
            self.write("User Not Found")
        elif user.courseinfo:
            self.load('main.html', user)
        else:
            self.redirect('/%s/settings' % userid)


class CourseHandler(Handler):
    def get(self, userid, courseid):
        user = query_id(userid)
        if user.courseinfo:
            self.load('main.html', user, active=courseid)
        else:
            self.redirect('/%s/settings' % userid)


class SettingsHandler(Handler):
    def get(self, userid):
        user = query_id(userid)
        remck = self.get_ck("rememberme")
        if not user:
            self.write("Registering... Please refresh in five seconds. Thanks! :P")
        if remck and int(remck)==user.rememberme:
            self.load('setup.html', user=user, active="settings")
        else:
            self.render('signup.html',page="login")

    def post(self, userid):
        user = query_id(userid)
        if 'update' in self.request.POST:       # update courseinfo
            # @TODO: make sure course order doens't change
            # @TODO: make courses sortable
            args = self.request.arguments()
            total = len(filter(lambda x: "course" in x, args))
            btn_args = filter(lambda x: "btn" in x and "url" not in x, args)
            courseinfo = []
            for i in range(total):
                courseID = self.request.get("course%d" % i)
                if courseID:
                    btns = []
                    btn_lst = filter(lambda x: "btn%d" % i in x, btn_args)
                    for btn_ind in range(len(btn_lst)):
                        logging.info("btn_ind:%d"%btn_ind)
                        btn = "btn%d-%d"%(i,btn_ind)
                        btn_name = self.request.get(btn)
                        btn_url = self.request.get(btn.replace("btn", "btn_url"))
                        if btn_name and btn_url:
                            btns.append((btn_name,btn_url))
                    courseinfo.append((courseID,btns))
            user.courseinfo = json.dumps(courseinfo)
            user.put()
            self.redirect("/%s" % userid)
        elif 'upload' in self.request.POST:         # upload schedule picture
            img = str(self.request.get("scheduleImage"))
            user.schedule = img
            user.put()
            self.redirect('/%s'%userid)
        elif 'general' in self.request.POST:
            # @TODO: user information update
            pass
        else:
            self.write("nothing?")


# Handles image fetch
class Image(webapp2.RequestHandler):
    def get(self):
        user_key = ndb.Key(urlsafe=self.request.get('img_id'))
        user = user_key.get()
        if user.schedule:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(user.schedule)
        else:
            self.response.out.write('No image')

class Datafix(Handler):
    def get(self,userid):
        user = query_id(userid)
        if user and user.courseinfo:
            if type(user.courseinfo)==dict:     # if user's courseinfo is still a dictionary
                new_lst = []                    # [(course1,[...]),(course2,[...])]
                for course in user.courseinfo:
                    new_btns = []               # [(btn1,link1),(btn2,link2)]
                    urls = user.courseinfo[course]
                    for btn in urls:         # course == {btn1:link1,btn2,link2}
                        new_btns.append((btn,urls[btn]))
                    new_lst.append((course,new_btns))
                user.courseinfo = new_btns
                self.write("new_list:"+user.courseinfo)

            elif type(user.courseinfo)==list:
                self.write("courseinfo is already in list")
            else:
                self.write("what type it is? "+ type(user.courseinfo))
        else:
            self.write("user not found or user does not have courseinfo")


app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/img', Image), webapp2.Route('/<userid>', UserHandler),
    webapp2.Route('/<userid>/settings', SettingsHandler), webapp2.Route('/<userid>/<courseid>', CourseHandler),
    webapp2.Route('/<userid>/datafix', Datafix)
], debug=True)
