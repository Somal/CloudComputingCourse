import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb


class Greeting(ndb.Model):
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        """Return a friendly HTTP greeting."""
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('Hello, World!')


class Clear(webapp2.RequestHandler):
    def post(self):
        greetings_query = Greeting.query(
            ancestor=guestbook_key()).fetch(keys_only=True)
        ndb.delete_multi(greetings_query)
        self.redirect('/')


def handle_404(request, response, exception):
    """Return a custom 404 error."""
    response.write('Sorry, nothing at this URL.')
    response.set_status(404)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/clear', Clear),
], debug=True)
application.error_handlers[404] = handle_404
