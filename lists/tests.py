import re

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page


# Create your tests here.

class HomePageTest(TestCase):
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')

    def test_root_url_resloves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        # response = home_page(request)
        # expected_html = render_to_string('home.html')


        # request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'
        response = home_page(request)

        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': '신규 작업 아이템'}
        )
        self.assertEqual(
            re.sub(self.pattern_input_csrf, '', response.content.decode()),
            re.sub(self.pattern_input_csrf, '', expected_html)
        )

        # self.assertEqual(response.content.decode(), expected_html)

    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = home_page(request)
    #     expected_html = render_to_string('home.html')
    #     self.assertEqual(response.content.decode(), expected_html)
    # self.assertTrue(response.content.strip().startswith(b'<html>'))
    # self.assertIn(b'<title>To-Do lists</title>', response.content)
    # self.assertTrue(response.content.strip().endswith(b'</html>'))
    # #
