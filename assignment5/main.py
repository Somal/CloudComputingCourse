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
    def get(self):
        greetings_query = Greeting.query(
            ancestor=guestbook_key()).fetch(keys_only=True)
        ndb.delete_multi(greetings_query)
        self.redirect('/')


class Results(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('results.html')
        all_data = Greeting.query(ancestor=guestbook_key()).fetch()
        result = {"data": [], "statistics": {}}
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

            names = {"question1": "Rate this project form 0 to 10",
                     "question2": "Can you briefly describe your experience in this project?",
                     "question3": "Tell us about the issues you faced while using the application",
                     "question4": "How often would you like to use this service?",
                     "question5": "Would you recommend this project to your friends ?"}
            renamed_responses = []
            for r in responses:
                row = {}
                for k, v in r.items():
                    row[names[k]] = v
                renamed_responses.append(row)

            statistics = {'mean': mean, 'Distribution_of_answers_on___would_you_like': question4_distribution,
                          'Distribution_of_answers_on___recommend': question5_distribution}
            result = {"data": renamed_responses, "statistics": statistics}
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
