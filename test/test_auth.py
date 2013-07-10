__author__ = 'isaacdontjelindell'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import string
import random

import unittest


def generateName():
    lst = [random.choice(string.ascii_letters) for n in xrange(20)]
    return "".join(lst)

def generateEmail():
    return generateName() + "@testing.com"


class LocalAuthTests(unittest.TestCase):

    def setUp(self):
        self.username = generateName()
        self.first_name = generateName()
        self.last_name = generateName()
        self.email = generateEmail()
        self.password = 't3stp4ssword'
        self.course_name = 'devcourse'
        self.host = 'http://127.0.0.1:8000'

        self.driver = webdriver.Firefox()

    def runTest(self):
        self.local_registration()
        self.logout()
        self.local_login()
        self.logout()

    def tearDown(self):
        self.driver.quit()

    def local_registration(self):
        self.driver.get(self.host + '/runestone/default/user/register')

        ## fill out the registration form ##
        self.driver.find_element_by_id('auth_user_username').\
            send_keys(self.username)
        self.driver.find_element_by_id('auth_user_first_name').\
            send_keys(self.first_name)
        self.driver.find_element_by_id('auth_user_last_name').\
            send_keys(self.last_name)
        self.driver.find_element_by_id('auth_user_email').\
            send_keys(self.email)
        self.driver.find_element_by_id('auth_user_password').\
            send_keys(self.password)
        self.driver.find_element_by_name('password_two').\
            send_keys(self.password)
        self.driver.find_element_by_id('auth_user_course_id').\
            send_keys(self.course_name)

        ## wait until the Captcha has been filled and we navigate away ##
        #element = self.driver.find_element_by_id('auth_user_username')
        #WebDriverWait(self.driver, 20).until(EC.staleness_of(element))

        ## submit the registration form ##
        self.driver.find_element_by_css_selector("input[value='Register']").\
            click()

        ## check that we were redirected to the course we just registered for ##
        expected_course_url = self.host + "/runestone/static/" + self.course_name
        self.assertIn(expected_course_url, self.driver.current_url,
            "Newly registered user not redirected to expected course (%s). Maybe there are errors " \
            "in the registration form?" % self.course_name)


    def local_login(self):
        self.driver.get(self.host + '/runestone/default/user/login')

        ## fill out the login form ##
        self.driver.find_element_by_id('auth_user_username'). \
            send_keys(self.username)
        self.driver.find_element_by_id('auth_user_password'). \
            send_keys(self.password)

        ## submit the login form ##
        self.driver.find_element_by_css_selector("input[value='Login']"). \
            click()

        ## check that we were redirected to the course this user is registered for ##
        expected_course_url = self.host + "/runestone/static/" + self.course_name
        self.assertIn(expected_course_url, self.driver.current_url,
                      "Not redirected to expected course (%s)." % self.course_name)


    def logout(self):
        self.driver.get(self.host + '/runestone/default/user/logout')

        ## check that the "Logged out" flash is visible
        try:
            flash_div = self.driver.find_element_by_class_name('flash')
            self.assertIn("Logged out", flash_div.text, "Logging out failed! Flash DIV had wrong text.")
        except NoSuchElementException:
            self.assertRaises(RuntimeError("Logging out failed! Could not find flash DIV."))
