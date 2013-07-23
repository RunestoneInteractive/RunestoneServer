from selenium import webdriver
import unittest


class DomAccessTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.host = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.driver.quit()

    #################################################################################################
    def test_dom_access(self):
        ''' quick test of the DOM access ability using the sample in overview '''
        self.driver.get(self.host + '/runestone/static/overview/overview.html')

        dom_input = self.driver.find_element_by_id('text1')
        dom_ac = self.driver.find_element_by_id('tftest1')

        dom_input.clear()
        dom_input.send_keys('testing')

        dom_ac.find_element_by_id('tftest1_runb').click()

        output = dom_ac.find_element_by_id('tftest1_pre').text

        self.assertTrue("value =  testing" in output,
                        "DOM access not working properly! Expected output '%s', got '%s'"
                        % ("value =  testing", output))

