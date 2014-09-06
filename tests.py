from main import application
from tornado.testing import AsyncHTTPTestCase

class MyHTTPTest(AsyncHTTPTestCase):
    def get_app(self):
        return application

    def test_homepage(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        # test contents of response
        assert response.body == 'Hello, world', response.body