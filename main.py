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

# user-input validation
import webapp2
import re
import cgi

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>User Signup</title>
        <style type="text/css">
            .error {
                color: red;
            }
            input {
                margin-left:50;
            }
        </style>
    </head>

    <body>
        <h1>
            Signup
        </h1>
"""

page_footer = """
    </body>
    </html>
"""

class Index(webapp2.RequestHandler):
    def get(self):
        user_name_form = """
            <form action="/add" method="post">
                <td>
                <label>
                    Username
                    <input type="text" name="user_name">
                    <span>%(name_error)s</span>
                </label>
                </td>
                <br>
                <label>
                    Password
                    <input type="text" name="user_pass">
                    <span>%(pass_error)s</span>
                </label>

                <br>
                <label>
                    Verify Password
                    <input type="text" name="user_pass_verify">
                </label>


                <br>
                <label>
                    E-mail
                    <input type="text" name="user_email">
                </label>
                <br>
            <input type="submit" value="Submit">
            </form>
            """

        #error = self.request.get("error")

        name_error = self.request.get("error")
        if name_error:
            error_esc = cgi.escape(name_error, quote=True)
            error_element = error_esc
        else:
            error_element = ""

        pass_error = self.request.get("")
        if pass_error:
            error_esc = cgi.escape(pass_error, quote=True)
            error_element_pass = error_esc
        else:
            error_element_pass = ""

        content = page_header + user_name_form + page_footer
        self.response.write(content)

class Add(webapp2.RequestHandler):
    def write_form(self, name_error="", pass_error=""):
        self.response.out.write(form % {"name_error" : name_error,
                                        "pass_error" : pass_error})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get("user_name")
        userpass = self.request.get("user_pass")
        userpassverify = self.request.get("user_pass_verify")
        useremail = self.request.get("user_email")
        if username == "":
            name_error = "The username is invalid."
            self.redirect("/?name_error=" + cgi.escape(name_error, quote=True))

        if userpass == "":
            pass_error = "Invalid password."
            self.redirect("/?error=" + cgi.escape(pass_error, quote=True))

        self.response.write(page_header + page_footer)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', Add)
], debug=True)
