#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from google.appengine.api.datastore import Key
from mygpu import MyGpu

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],autoescape=True)


class Compare(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        user = users.get_current_user()
        if user:
            url = users.create_logout_url('/')
            url_string = 'logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        choices = self.request.GET.getall('choice')
        for i in range(len(choices)):
            choices[i] = str(choices[i])
        id_choices=[]
        for i in choices:
            mygpu_key = ndb.Key('MyGpu', i)
            mygpu = mygpu_key.get()
            id_choices.append(mygpu)
        template_values = {
            'gpu_array' : id_choices,
            'mygpu': choices[0]
            }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('cancel'):
            return self.redirect('/table')
        self.redirect('/table')
