import os
import webapp2
from google.appengine.ext.webapp import template


class MainPage(webapp2.RequestHandler):
    def get(self):
        """Return a friendly HTTP greeting."""
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('Hello, World!')


def handle_404(request, response, exception):
    """Return a custom 404 error."""
    response.write('Sorry, nothing at this URL.')
    response.set_status(404)


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
application.error_handlers[404] = handle_404
