from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import unittest


class AssessTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.host = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.driver.quit()

    #################################################################################################

    def test_MCMF(self):
        self.driver.get(self.host + '/runestone/static/overview/overview.html')

        # MCMF question
        question = self.driver.find_element_by_id('question1_1')

        # select the correct answer
        question.find_element_by_id('question1_1_opt_a').click()

        # submit the answer
        submit_button = question.find_element_by_name('do answer')
        submit_button.click()

        # check that feedback is correct
        feedback = question.find_element_by_id('question1_1_feedback').text
        self.assertTrue("Correct!!" in feedback, "MCMF correct answer not graded correctly!")

        # select an incorrect answer
        question.find_element_by_id('question1_1_opt_b').click()

        # submit the answer
        submit_button.click()

        # check that feedback is incorrect
        feedback = question.find_element_by_id('question1_1_feedback').text
        self.assertTrue("Incorrect." in feedback, "MCMF incorrect answer not graded correctly!")
