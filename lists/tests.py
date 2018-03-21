import re

from django.core.urlresolvers import resolve
from django.http import HttpRequest
# from django.template.loader import render_to_string
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page, view_list
from lists.models import Item, List


# Create your tests here.

class HomePageTest(TestCase):
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')

    def test_root_url_resloves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'new_item_text': '신규 작업 아이템'})
        # expected_html = render_to_string('home.html')


        # self.assertEquals(response.content.decode(), expected_html)
    #
    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)

    # def test_home_page_displays_all_list_items(self):
    #     list_ = List.objects.create()
    #     Item.objects.create(text='itemey 1',list=list_)
    #     Item.objects.create(text='itemey 2',list=list_)
    #
    #     request = HttpRequest()
    #     response = view_list(request)
    #     # print(response)
    #     print(response.content.decode())
    #
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.list = list_
        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, '두 번째 아이템')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()

        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='다른 목록 아이템1', list=other_list)
        Item.objects.create(text='다른 목록 아이템2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, '다른 목록 아이템1')
        self.assertNotContains(response, '다른 목록 아이템2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

        # self.assertIn('itemey 1', str(response.content.decode()))
        # self.assertIn('itemey 2', response.content.decode())


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        # self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': '기존 목록에 신규 아이템'}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
