import json
import os

import jinja2
import webapp2
from google.appengine.ext import ndb

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
        all_data = Greeting.query(ancestor=guestbook_key()).fetch()
        result = {}
        if all_data.__len__() > 0:
            responses = [json.loads(d.content) for d in all_data]

            mean = 0
            question4_distribution = {u"1": 0, u"2": 0, u"3": 0}
            question5_distribution = {u"1": 0, u"2": 0}
            for r in responses:
                mean += int(r.get('question1'))
                question4_distribution[r.get('question4')] += 1
                question5_distribution[r.get('question5')] += 1

            count = responses.__len__() * 1.0
            mean = mean / count
            for k in question4_distribution.keys():
                question4_distribution[k] = question4_distribution[k] / count

            for k in question5_distribution.keys():
                question5_distribution[k] = question5_distribution[k] / count

            statistics = {'mean': mean, 'question4_distribution': question4_distribution,
                          'question5_distribution': question5_distribution}
            result = {"data": responses, "statistics": statistics}
        print(result)
        self.response.out.write(template.render(entries=result))


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
