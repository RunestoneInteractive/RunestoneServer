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
        self.assertTrue("Correct!!" in feedback,
                        "MCMF correct answer not graded correctly!")

        # select an incorrect answer
        question.find_element_by_id('question1_1_opt_b').click()

        # submit the answer
        submit_button.click()

        # check that feedback is incorrect
        feedback = question.find_element_by_id('question1_1_feedback').text
        self.assertTrue("Incorrect." in feedback,
                        "MCMF incorrect answer not graded correctly!")


    def test_MCMA(self):
        self.driver.get(self.host + '/runestone/static/overview/overview.html')

        question = self.driver.find_element_by_id('question1_2')

        # select the correct answers
        question.find_element_by_id('question1_2_opt_a').click()
        question.find_element_by_id('question1_2_opt_b').click()
        question.find_element_by_id('question1_2_opt_d').click()

        # submit answers
        submit_button = question.find_element_by_name('do answer')
        submit_button.click()

        # check that feedback is correct
        feedback = question.find_element_by_id('question1_2_feedback').text
        self.assertTrue("Correct!" in feedback,
                        "MCMA correct answers not graded correctly!")

        # select a wrong answer
        question.find_element_by_id('question1_2_opt_c').click()

        # submit answer
        submit_button.click()

        # check that feedback is incorrect
        feedback = question.find_element_by_id('question1_2_feedback').text
        self.assertTrue("Incorrect." in feedback,
                        "MCMA incorrect answer not graded correctly!")

    def test_FIB(self):
        self.driver.get(self.host + '/runestone/static/overview/overview.html')

        question = self.driver.find_element_by_id('baseconvert1')

        # input the correct answer
        question.find_element_by_id('baseconvert1_ans1').send_keys('31')

        # submit the answer
        submit_button = question.find_element_by_name('do answer')
        submit_button.click()

        # check that feedback is correct
        feedback = question.find_element_by_id('baseconvert1_feedback').text
        self.assertTrue('You are Correct' in feedback,
                        "FIB correct answer not graded correctly!")

        # input the wrong answer
        question.find_element_by_id('baseconvert1_ans1').send_keys('50')

        # submit the answer
        submit_button = question.find_element_by_name('do answer')
        submit_button.click()

        # check that feedback is incorrect
        feedback = question.find_element_by_id('baseconvert1_feedback').text
        self.assertTrue('Incorrect.' in feedback,
                        "FIB incorrect answer not graded correctly!")


    def test_codelens(self):
        self.driver.get(self.host + '/runestone/static/overview/overview.html')

        question = self.driver.find_element_by_id('firstexample')

        forward_button = question.find_element_by_id('jmpStepFwd')

        forward_button.click()
        output = question.find_element_by_id('pyStdout').get_attribute('value')
        expected_output = 'My first program adds two numbers, 2 and 3:\n'
        self.assertTrue(expected_output in output, "Codelens output is incorrect!")

        forward_button.click()
        output = question.find_element_by_id('pyStdout').get_attribute('value')
        expected_output = 'My first program adds two numbers, 2 and 3:\n5\n'
        self.assertTrue(expected_output in output, "Codelens output is incorrect!")

        # test inline "Check Your Understanding" question
        question = self.driver.find_element_by_id('codelens_question')
        forward_button = question.find_element_by_id('jmpStepFwd')


        modal = self.driver.find_element_by_id('codelens_question_modal')
        disp = modal.value_of_css_property('display')
        self.assertTrue(disp == 'none',
                        "'Check Your Understanding modal is visible when it shouldn't be!")

        forward_button.click()
        forward_button.click()
        forward_button.click()

        modal = self.driver.find_element_by_id('codelens_question_modal')
        disp = modal.value_of_css_property('display')
        self.assertTrue(disp == 'block')

        self.assertTrue("What is the value of tot" in modal.text)

        modal_input = modal.find_element_by_id('codelens_question_textbox')
        modal_input.send_keys('0')

        check_button = modal.find_element_by_id('codelens_question_tracecheck')
        check_button.click()

        feedback_text = modal.find_element_by_id('codelens_question_feedbacktext').text
        self.assertTrue('Correct' in feedback_text,
                        "The correct answer feedback for 'Check Your Understanding' question is wrong!")

        modal_input.send_keys('5')
        check_button.click()

        feedback_text = modal.find_element_by_id('codelens_question_feedbacktext').text
        self.assertTrue('Use the global variables box to look' in feedback_text,
                        "The incorrect answer feedback for 'Check Your Understanding' question is wrong!")

