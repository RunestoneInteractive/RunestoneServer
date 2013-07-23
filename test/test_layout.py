__author__ = 'isaacdontjelindell'

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest


class LayoutTests(unittest.TestCase):
    def setUp(self):
        self.host = 'http://127.0.0.1:8000'
        self.course_name = ''
        self.driver = webdriver.Firefox()

    def test_thinkcspy(self):
        self.course_name = 'thinkcspy'

        self.logo_link()
        self.course_title_link()
        self.search_menu()
        self.social_media_menu()
        self.help_menu()

    def test_pythonds(self):
        self.course_name = 'pythonds'

        self.logo_link()
        self.course_title_link()
        self.search_menu()
        self.social_media_menu()
        self.help_menu()

    def tearDown(self):
        self.driver.quit()

    ##########################################################################################

    def logo_link(self):
        ''' test that the RSI logo in the navbar links to the RSI site '''

        self.driver.get('%s/runestone/static/%s/index.html'
                        % (self.host, self.course_name))

        self.driver.find_element_by_class_name('brand-logo').click()

        # make sure the logo link goes to the right place
        expected_url = '%s/runestone/default/user/login' % self.host
        self.assertEqual(self.driver.current_url, expected_url, 'Logo link does not go to'
                                                                ' the correct location! Expected %s, got %s.' % (
                                                                expected_url, self.driver.current_url))

    def course_title_link(self):
        ''' test that clicking on the course title links to the Sphinx master doc (index or toc.html) '''

        self.driver.get('%s/runestone/static/%s/index.html'
                        % (self.host, self.course_name))

        title_link = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_class_name('brand'))
        title_link.click()

        if 'pythonds' in self.course_name:
            expected_url = '%s/runestone/static/%s/index.html#' % (self.host, self.course_name)
        else:
            expected_url = '%s/runestone/static/%s/toc.html' % (self.host, self.course_name)

        self.assertEqual(self.driver.current_url, expected_url, "Title link does not go to "
                                                                "the correct location! Expected %s, got %s." % (
                                                                expected_url, self.driver.current_url))

    def social_media_menu(self):
        ''' test that the Facebook and Twitter buttons are visible in the social media dropdown menu '''

        self.driver.get('%s/runestone/static/%s/index.html'
                        % (self.host, self.course_name))

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

    def search_menu(self):
        ''' test the links and functionality of the search dropdown menu '''

        def open_menu():
            self.driver.get('%s/runestone/static/%s/index.html'
                            % (self.host, self.course_name))

            # trigger the menu to open
            menu_toggles = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_elements_by_class_name('dropdown-toggle'))
            menu_toggles[1].click()

            # make sure it actually did open
            dropdown_el = self.driver.find_element_by_class_name('open')

            # get the list with the menu items
            search_menu = dropdown_el.find_element_by_class_name('dropdown-menu')

            return search_menu

        # Table of Contents link
        search_menu = open_menu()
        search_menu.find_elements_by_tag_name('a')[0].click()
        if 'pythonds' in self.course_name:
            expected_url = '%s/runestone/static/%s/index.html#' % (self.host, self.course_name)
        else:
            expected_url = '%s/runestone/static/%s/toc.html' % (self.host, self.course_name)
        self.assertEqual(expected_url, self.driver.current_url,
                         "Wrong 'Table of Contents' link: expected %s, got %s." % (
                         expected_url, self.driver.current_url))

        # Book Index link
        search_menu = open_menu()
        search_menu.find_elements_by_tag_name('a')[1].click()
        expected_url = '%s/runestone/static/%s/genindex.html' % (self.host, self.course_name)
        self.assertEqual(expected_url, self.driver.current_url,
                         "Wrong 'Book Index' link: expected %s, got %s." % (expected_url, self.driver.current_url))

    def help_menu(self):
        ''' test that links in the help menu work and link to the correct locations '''

        def open_menu():
            self.driver.get('%s/runestone/static/%s/index.html'
                            % (self.host, self.course_name))

            # trigger the menu to open
            menu_toggles = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_elements_by_class_name('dropdown-toggle'))
            menu_toggles[3].click()

            # make sure it actually did open
            dropdown_el = self.driver.find_element_by_class_name('open')

            # get the list with the menu items
            help_menu = dropdown_el.find_element_by_class_name('user-menu')

            return help_menu

        # Navigation Help link
        help_menu = open_menu()
        help_menu.find_elements_by_tag_name('a')[0].click()
        expected_url = '%s/runestone/static/%s/navhelp.html' % (self.host, self.course_name)
        self.assertEqual(expected_url, self.driver.current_url,
                         "Wrong 'Navigation Help' link: expected %s, got %s" % (expected_url, self.driver.current_url))

        # Instructor's Page link
        help_menu = open_menu()
        link = help_menu.find_elements_by_tag_name('a')[1].get_attribute('href')
        expected_url = '%s/runestone/admin/index' % self.host
        self.assertEqual(expected_url, link,
                         "Wrong 'Navigation Help' link: expected %s, got %s" % (expected_url, link))

        # About Runestone link
        help_menu = open_menu()
        help_menu.find_elements_by_tag_name('a')[2].click()
        expected_url = 'http://runestoneinteractive.org/'
        self.assertEqual(expected_url, self.driver.current_url,
                         "Wrong 'About Runestone' link: expected %s, got %s" % (expected_url, self.driver.current_url))

        # Report A Problem link
        help_menu = open_menu()
        link = help_menu.find_elements_by_tag_name('a')[3].get_attribute('href')
        expected_url = 'https://github.com/bnmnetp/runestone/issues/new'
        self.assertEqual(expected_url, link,
                         "Wrong 'Report A Problem' link: expected %s, got %s" % (expected_url, link))
