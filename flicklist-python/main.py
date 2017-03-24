import webapp2
import random

class Index(webapp2.RequestHandler):

    def getRandomMovie(self):

        # TODO: make a list with at least 5 movie titles
        movie_list = ("Rogue One", "Alien", "Indiana Jones: Raiders of the Lost Arc", "Star Wars: Empire Strikes Back", "X-Men: Days of Future's Past")
        # TODO: randomly choose one of the movies, and return it
        movie_num = random.randint (0, 4)
        return movie_list[movie_num]

    def get(self):
        # choose a movie by invoking our new function
        movie = self.getRandomMovie()

        # build the response string
        content = "<h1>Movie of the Day</h1>"
        content += "<p>" + movie + "</p>"

        # TODO: pick a different random movie, and display it under
        # the heading "<h1>Tommorrow's Movie</h1>"

        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
