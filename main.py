#!/usr/bin/env python

import webapp2
import re
from google.appengine.api import urlfetch
import json

REFERER_REGEX = "^https?://github.com/D-Programming-Language/(dmd|phobos|druntime)/pull/(\d{1,5})$"

class FrontHandler(webapp2.RequestHandler):
    def get(self):

        referer = self.request.environ['HTTP_REFERER'] \
            if 'HTTP_REFERER' in self.request.environ else  None
        if not referer:
            self.instructions()
            return

        m = re.match(REFERER_REGEX, referer)
        if not m:
            self.instructions()
            return

        repo = m.group(1)
        pull = m.group(2)

        self.redirect(r'/%s/%s.png' % (repo, pull))

    def instructions(self):
        self.response.out.write("""
<!DOCTYPE html>
<html>
<head>
    <link href='https://fonts.googleapis.com/css?family=Doppio+One' rel='stylesheet' type='text/css'>
    <title>D Autotester Badges</title>
    <style>
        body {
            font-size: 25px;
            font-family: 'Doppio One', sans-serif;
        }
        #instructions {
            position:absolute;
            top:0; bottom:0; right:0; left:0;
            margin:auto;
            height: 1em;
            padding: 2em;
            width: 700px;
            border-radius: 15px;
            box-shadow: 0px 0px 15px 10px #f6f6f6;
            text-align: center;
            vertical-align: middle;
        }
    </style>
</head>
<body>
<div id="instructions">
    ![Test Results](https://dtestbadge.appspot.com)
</div>""")

class BadgeHandler(webapp2.RequestHandler):
    def get(self, repo, pull):
        url = "http://d.puremagic.com/test-results/pull.json.ghtml?ref=https://github.com/D-Programming-Language/%s/pull/%s" % (repo, pull)
        result = urlfetch.fetch(url)
        if result.status_code != 200:
            self.unknown()
            return


        passes = True
        outdated = False

        test_data = json.loads(result.content)

        if len(test_data) == 0 or not test_data.get('results'):
            self.unknown()
            return

        for platform in test_data['results']:
            passes &= platform['rc'] == '0' or platform['rc'] == ''
            outdated |= platform['deleted'] == '1'

        self.response.headers["Content-Type"] = "image/png"
        img = 'tests-%s%s.png' % ('pass' if passes else 'fail',
                                  '-outdated' if outdated else '')
        with open(img, 'rb') as f:
            self.response.out.write(f.read());

    def unknown(self):
        self.response.headers["Content-Type"] = "image/png"
        img = 'tests-unknown.png'
        with open(img, 'rb') as f:
            self.response.out.write(f.read());


app = webapp2.WSGIApplication(
        [(r'/', FrontHandler),
         (r'/(dmd|phobos|druntime)/(\d{1,5})(?:\.png)?', BadgeHandler)],
        debug=True)
