__author__ = 'isaacdontjelindell'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string
import random


def generateName():
    lst = [random.choice(string.ascii_letters) for n in xrange(20)]
    return "".join(lst)

def generateEmail():
    return generateName() + "@testing.com"


class LocalUser:

    def __init__(self, username=None, first_name=None, last_name=None,
                 email=None, password='t3stp4ssword', course_name='devcourse'):

        if username is None:
            username = generateName()
        if first_name is None:
            first_name = generateName()
        if last_name is None:
            last_name = generateName()
        if email is None:
            email = generateEmail()

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.course_name = course_name

        self.driver = webdriver.Firefox()
        self.host = 'http://127.0.0.1:8000'


    def register(self):
        self.driver.get(self.host + '/runestone/default/user/register')

        ## Fill out the registration form ##
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
        element = self.driver.find_element_by_id('auth_user_username')
        WebDriverWait(self.driver, 20).until(EC.staleness_of(element))

        assert (self.host + "/runestone/static/" + self.course_name) in self.driver.current_url, \
            "Newly registered user not redirected to expected course."


