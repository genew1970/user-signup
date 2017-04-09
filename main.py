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

header = """
<!DOCTYPE html>
<html>
    <head>
        <title>User Signup</title>
        <style type="text/css">
            .error {
                color: red;
            }

            .input_label {
                text-align: right;
            }

        </style>
    </head>
"""

footer = """
    </body>
    </html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
    return user_name and USER_RE.match(user_name)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(user_pass):
    return user_pass and PASS_RE.match(user_pass)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(user_email):
    return not user_email or EMAIL_RE.match(user_email)

class Index(webapp2.RequestHandler):
    def user_form(self, user_name="", user_pass="", user_pass_verify="", user_email="", name_error="", pass_error="", pass_match_error="", email_error=""):
        form = """
            <body>
                <h1>
                    Signup
                </h1>

                <form action-"/add" method="post">
                    <table>
                        <tr>
                            <td class="input_label">
                                Username
                            </td>

                            <td>
                                <input type="text" name="user_name" value="%(user_name)s">
                                <span class="error">%(name_error)s</span>
                            </td>
                        </tr>

                        <tr>
                            <td class="input_label">
                                Password
                            </td>

                            <td>
                                <input type="password" name="user_pass">
                                <span class="error">%(pass_error)s</span>
                            </td>
                        </tr>

                        <tr>
                            <td class="input_label">
                                Verify Password
                            </td>

                            <td>
                                <input type="password" name="user_pass_verify">
                                <span class="error">%(pass_match_error)s</span>
                            </td>
                        </tr>

                        <tr>
                            <td class="input_label">
                                E-mail (optional)
                            </td>

                            <td>
                                <input type="text" name="user_email" value="%(user_email)s">
                                <span class="error">%(email_error)s</span>
                            </td>
                        </tr>
                    </table>

                <br>
                <input type="submit" value="Submit">
                </form>
        """
        signup_form = header + form + footer
        self.response.out.write(signup_form % {"user_name": cgi.escape(user_name,quote = True),
                                        "user_pass": cgi.escape(user_pass,quote = True),
                                        "user_pass_verify": cgi.escape(user_pass_verify,quote = True),
                                        "user_email": cgi.escape(user_email,quote = True),
                                        "name_error": name_error,
                                        "pass_error": pass_error,
                                        "pass_match_error": pass_match_error,
                                        "email_error": email_error})

    def get(self):
        self.user_form()

    def post(self):
        invalid_entry = False
        user_name = self.request.get("user_name")
        user_pass = self.request.get("user_pass")
        user_pass_verify = self.request.get("user_pass_verify")
        user_email = self.request.get("user_email")
        name_error=""
        pass_error=""
        pass_match_error=""
        email_error=""

        if not valid_username(user_name):
            invalid_entry = True
            name_error = "That is not a valid username."

        if not valid_password(user_pass):
            invalid_entry = True
            pass_error = "That was not a valid password."

        if user_pass != user_pass_verify:
            invalid_entry = True
            pass_match_error = "Your passwords did not match."

        if not valid_email(user_email):
            invalid_entry = True
            email_error = "That is not a valid email."

        if invalid_entry == True:
            self.user_form(user_name, user_pass, user_pass_verify, user_email,
                            name_error, pass_error, pass_match_error, email_error)
        else:
            self.redirect("/add?user_name=" + user_name)

class Add(webapp2.RequestHandler):

    def add_page(self, user_name=""):
        user_name = self.request.get("user_name")
        success_form = """
            <h1>Welcome, %(user_name)s!</h1>
        """

        welcome_form = header + success_form + footer
        self.response.out.write(welcome_form % {"user_name": user_name})

    def get(self):
        self.add_page()


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', Add)
], debug=True)
