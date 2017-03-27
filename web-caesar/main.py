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
import caesar
import cgi

def build_page(textarea_content):
    # input to allow the user to input the number to rotate by.
    # the value is initially set to zero
    rot_label = "<label>Rotate by:</label>"
    rotation_input = "<input class='user_input' type='number' value='0' name='rotation'/>"

    # text area holds the message to be displayed with a label messad
    message_label = "<label>Type a message:</label>"
    textarea = "<textarea class='user_input' name='message'>" + textarea_content + "</textarea>"

    # button to submit the form and add content to send to the html to be returned
    submit = "<input class='button' type='submit'/>"
    form = ("<form method='post'>" + rot_label + "<br>" + rotation_input + "<br><br>" +
        message_label + "<br>" + textarea + "<br>" + submit + "</form>")

    # adds html style content, header and title to the web app
    header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FlickList</title>
        <style>

            h1 {
                font-size: 48px;
                color: blue;
                text-shadow: 1px 1px 5px red;
            }

            label {
                font-size: 36px;
                color: crimson;
                text-shadow: 1px 1px 5px black;
            }

            .button {
                font-size: 15px;
                color: white;
                background-color: blue;
            }

            .user_input {
                font-size: 24px;
                color: blue;
                text-shadow: 1px 1px 3px crimson;
            }

        </style>
    </head>
    <body>
        <h1>Web Caesar</h1>
    """
    footer = """
    </body>
    </html>
    """

    # returns the header, form and footer
    return header + form + footer

class MainHandler(webapp2.RequestHandler):
    # get method to initialize page
    def get(self):
        content = build_page("")
        self.response.write(content)

    # post method once the form has been submitted.  escape is used to keep users
    # from entering html code to change the format of the page
    def post(self):
        message = self.request.get("message")
        rotation = int(self.request.get("rotation"))
        encrypted_message = caesar.encrypt(message, rotation)
        escaped_message = cgi.escape(encrypted_message)
        content = build_page(escaped_message)
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
