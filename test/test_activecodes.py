from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import unittest


class ActiveCodeTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.host = 'http://127.0.0.1:8000'
        self.courses_to_test = ['thinkcspy', 'pythonds']

    def runTest(self):
        '''
        1. Get a list of all the chapters/pages in all the courses specified in self.courses_to_test
        2. Find and run every ActiveCode block on each page
        3. Print out information about any ActiveCode that results in an error.
        :return:
        '''
        link_list = []
        for course in self.courses_to_test:
            if 'pythonds' in course:
                self.driver.get(self.host + "/runestone/static/%s/index.html" % course)
            else:
                self.driver.get(self.host + "/runestone/static/%s/toc.html" % course)

            ## get the list of pages to test ##
            chapters = self.driver.find_elements_by_class_name('toctree-l1')
            for c in chapters:
                l = c.find_element_by_tag_name('a')
                link_list.append(l.get_attribute('href'))

        for l in link_list:
            self.runActiveCodesOnPage(l)

    def tearDown(self):
        self.driver.quit()

    #################################################################################################

    def runActiveCodesOnPage(self, url):
        '''Find and run every ActiveCode element on the page specified by url'''
        self.driver.get(url)
        course_name = url.split('static')[1].split('/')[1]

        allButtons = self.driver.find_elements_by_tag_name("button")

        for button in allButtons:
            try:
                if button.text == "Run":
                    button.click()

                    alert = self.driver.switch_to_alert() # some ActiveCode blocks expect input

                    # this is just random text; using an integer string because some AC blocks do int casting
                    alert.send_keys('1111')
                    alert.dismiss()

            except WebDriverException:
                # no input prompt for this ActiveCode
                pass

        ## find any error DIVS ##
        allErrors = self.driver.find_elements_by_class_name("error")
        for e in allErrors:
            print "[%s] Error in ActiveCode [%s] on page [%s]." \
                  % (course_name, e.get_attribute('id'), url[url.rindex('/') + 1:])

