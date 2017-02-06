import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
import jinja2
import json

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def guestbook_key(guestbook_name='default_guestbook'):
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.StringProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        """Return a friendly HTTP greeting."""
        greetings_query = Greeting.query(
            ancestor=guestbook_key()).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(entries=greetings))

    def post(self):
        greeting = Greeting(parent=guestbook_key())
        # response = json.loads(self.request.get('data'))
        greeting.content = self.request.get('data')
        greeting.put()
        self.redirect('/')


class Clear(webapp2.RequestHandler):
    def post(self):
        greetings_query = Greeting.query(
            ancestor=guestbook_key()).fetch(keys_only=True)
        ndb.delete_multi(greetings_query)
        self.redirect('/')

class Results(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('results.html')
        self.response.out.write(template.render(entries=None))

def handle_404(request, response, exception):
    """Return a custom 404 error."""
    response.write('Sorry, nothing at this URL.')
    response.set_status(404)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/clear', Clear),
    ('/results', Results),
], debug=True)
application.error_handlers[404] = handle_404
