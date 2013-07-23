from selenium import webdriver
import unittest


class RevealTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.host = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.driver.quit()

    #################################################################################################
    def test_reveal(self):
        ''' test the reveal directive '''
        self.driver.get(self.host + '/runestone/static/overview/overview.html')

        reveal_div = self.driver.find_element_by_id('revealid1')

        disp = reveal_div.value_of_css_property('display')
        self.assertTrue(disp == 'none',
                        "Reveal div should not be visible until the show button is clicked!")

        show_b = self.driver.find_element_by_id('revealid1_show')
        hide_b = self.driver.find_element_by_id('revealid1_hide')

        show_b.click()
        disp = reveal_div.value_of_css_property('display')
        self.assertTrue(disp == 'block',
                        "Reveal div should be visible after show button is clicked!")

        hide_b.click()
        disp = reveal_div.value_of_css_property('display')
        self.assertTrue(disp == 'none',
                        "Reveal div should not be visible after the hide button is clicked!")
