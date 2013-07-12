__author__ = 'isaacdontjelindell'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import string
import random
import unittest

class LayoutTests(unittest.TestCase):

    def setUp(self):
        self.host = 'http://127.0.0.1:8000'
        self.course_name = 'thinkcspy'
        self.driver = webdriver.Firefox()

    def runTest(self):
        self.logo_link()
        self.course_title_link()
        self.social_media_menu()

    def tearDown(self):
        self.driver.quit()

    ##################################################################

    def logo_link(self):
        self.driver.get('%s/runestone/static/%s/index.html'
                        %(self.host, self.course_name))

        self.driver.find_element_by_class_name('brand-logo').click()

        # make sure the logo link goes to the right place
        expected_url = 'http://runestoneinteractive.org/'
        self.assertEqual(self.driver.current_url, expected_url, 'Logo link does not go to'
                    ' the correct location! Expected %s, got %s.' % (expected_url, self.driver.current_url))

    def course_title_link(self):
        self.driver.get('%s/runestone/static/%s/index.html'
                        %(self.host, self.course_name))

        title_link = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name('brand'))
        title_link.click()


        if 'pythonds' in self.course_name:
            expected_url = '%s/runestone/static/%s/index.html' % (self.host, self.course_name)
        else:
            expected_url = '%s/runestone/static/%s/toc.html' % (self.host, self.course_name)

        self.assertEqual(self.driver.current_url, expected_url, "Title link does not go to "
                    "the correct location! Expected %s, got %s." % (expected_url, self.driver.current_url))

    def social_media_menu(self):
        self.driver.get('%s/runestone/static/%s/index.html'
                        %(self.host, self.course_name))

        # trigger the menu to open
        menu_toggles = WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_class_name('dropdown-toggle'))
        menu_toggles[0].click()

        # make sure it actually did open
        dropdown_el = self.driver.find_element_by_class_name('open')

        # get the div holding the social media buttons
        social_div = dropdown_el.find_element_by_class_name('social-menu')

        # make sure the Twitter button is visible
        twitter_button = social_div.find_element_by_class_name('twitter-follow-button')
        self.assertTrue(twitter_button.is_displayed(), 'The Twitter follow button is not displayed!')

        # make sure the Facebook like button is visible
        fb_button = social_div.find_element_by_class_name('fb-like')
        self.assertTrue(fb_button.is_displayed(), "The Facebook 'Like' button is not displayed!")