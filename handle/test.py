# -*- coding: utf-8 -*-
# Created on 2017-7-12
# @author: lsy
from base import BaseHandler
from tornado.web import authenticated



class IndexHandle(BaseHandler):
    @authenticated
    def get(self):
        if self.get_secure_cookie('role') != '2':
            self.redirect('/index')
        username = self.get_secure_cookie('username')
        info = {
            'username': username
        }
        self.render('merchant-account-book.html', **info)