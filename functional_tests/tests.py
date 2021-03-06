import time

from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('1: 공작깃털 사기', [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(2)

        edith_list_url = self.browser.current_url
        # print(edith_list_url)
        self.assertRegex(edith_list_url, '/list/.+')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        time.sleep(2)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물만들기')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(2)

        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물만들기')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('1: 공작깃털 사기', [row.text for row in rows])
        # self.assertIn(
        #     '2: 공작깃털을 이용해서 그물 만들기',
        #     [row.text for row in rows]
        # )
        self.fail('Finish the test!')

# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
