from selenium import webdriver
import unittest


class PollTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.host = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.driver.quit()

    #################################################################################################
    def test_poll(self):
        ''' test the poll directive '''
        self.driver.get(self.host + '/runestone/static/overview/overview.html')

        poll_div = self.driver.find_element_by_id('pollid1')

        opts = poll_div.find_elements_by_css_selector(".poll-options input[type='radio']")

        # the poll in overview should be on a scale 1-10.
        self.assertTrue(len(opts) == 10, "Not enough poll options present!")

        # just choose option 4
        poll_div.find_element_by_id('pollid1_4').click()

        # submit
        poll_div.find_element_by_id('pollid1_submit').click()

        # just make sure we can find the results div - an exception will be raised if the div cannot be found
        poll_div.find_element_by_id('pollid1_results')

