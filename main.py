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

# html header form
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

# html footer form
footer = """
    </body>
    </html>
"""

# checks formatting of the user_name and returns true or false depending
# wether or not the criteria is met
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
    return user_name and USER_RE.match(user_name)

# checks formatting of the user_pass and returns true or false depending
# wether or not the criteria is met
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(user_pass):
    return user_pass and PASS_RE.match(user_pass)

# checks the integrity of the email field and returns true or false
# depending on the validity of the user input
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(user_email):
    return not user_email or EMAIL_RE.match(user_email)

# main handler for the home page
class Index(webapp2.RequestHandler):
    # initializes the user form to fill fields initially with no values as the default parameter
    def user_form(self, user_name="", user_pass="", user_pass_verify="", user_email="", name_error="", pass_error="", pass_match_error="", email_error=""):
        # form that contains labels with the appropriate inputs
        form = """
            <body>
                <h1>
                    Signup
                </h1>

                <form action-"/welcome" method="post">
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

        # concatenates the forms
        signup_form = header + form + footer

        # uses the escape (cgi) in a dictionary containing the input field variables
        # the error messages are set up to pass the results of error checks
        self.response.out.write(signup_form % {"user_name": cgi.escape(user_name,quote = True),
                                        "user_pass": cgi.escape(user_pass,quote = True),
                                        "user_pass_verify": cgi.escape(user_pass_verify,quote = True),
                                        "user_email": cgi.escape(user_email,quote = True),
                                        "name_error": name_error,
                                        "pass_error": pass_error,
                                        "pass_match_error": pass_match_error,
                                        "email_error": email_error})

    # call to create the user form
    def get(self):
        self.user_form()

    def post(self):
        # initializes the boolean value for valid entries and creates variables
        # to hold the values of the get requests.  error messages initialized
        invalid_entry = False
        user_name = self.request.get("user_name")
        user_pass = self.request.get("user_pass")
        user_pass_verify = self.request.get("user_pass_verify")
        user_email = self.request.get("user_email")
        name_error=""
        pass_error=""
        pass_match_error=""
        email_error=""

        # call to check for a valid user name
        if not valid_username(user_name):
            invalid_entry = True
            name_error = "That is not a valid username."

        # call to check for a valid password
        if not valid_password(user_pass):
            invalid_entry = True
            pass_error = "That was not a valid password."

        # evaluates the passwords to check for a match
        if user_pass != user_pass_verify:
            invalid_entry = True
            pass_match_error = "Your passwords did not match."

        # call to check for a valid email
        if not valid_email(user_email):
            invalid_entry = True
            email_error = "That is not a valid email."

        # should the invalid_entry trigger to True, the form will be called
        # and sends in the correct error messages
        if invalid_entry == True:
            self.user_form(user_name, user_pass, user_pass_verify, user_email,
                            name_error, pass_error, pass_match_error, email_error)
        else:
            # a successful entry will redirect the user to the /add page
            self.redirect("/welcome?user_name=" + user_name)

class Welcome(webapp2.RequestHandler):

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
    ('/welcome', Welcome)
], debug=True)
