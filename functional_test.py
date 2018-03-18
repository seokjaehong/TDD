from selenium import webdriver
import unittest


#
# browser = webdriver.Chrome()
# browser.get('http://localhost:8000')
# assert 'To-Do' in browser.title
# browser.quit()
from selenium.webdriver.common.keys import Keys


if __name__ == '__main__':
    unittest.main(warnings='ignore')

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-do', header_text)

        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )
        print(inputbox)

        inputbox.send_keys('공작 깃털 사기')

        inputbox.send_keys(Keys.ENTER)

        table =self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
            any(row.text=='1:공작깃털사기' for row in rows),
        )

        self.fail('Finish the test!')
