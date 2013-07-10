from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException
import time
import unittest


class ActiveCodeTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.host = 'http://127.0.0.1:8000'

    def runTest(self):
        self.driver.get(self.host + "/runestone/static/thinkcspy/toc.html")

        ## get the list of pages to test ##
        chapters = self.driver.find_elements_by_class_name('toctree-l1')
        link_list = []
        for c in chapters:
            l = c.find_element_by_tag_name('a')
            link_list.append(l.get_attribute('href'))

        for l in link_list:
            #print "Testing activecode blocks on page: ", l[l.rindex('/')+1:]
            self.runActiveCodesOnPage(l)

    def tearDown(self):
        self.driver.quit()


    def runActiveCodesOnPage(self, url):
        self.driver.get(url)

        allButtons = self.driver.find_elements_by_tag_name("button")

        for button in allButtons:
            try:
                if button.text == "Run":
                    button.click()

                    alert = self.driver.switch_to_alert() # some ActiveCode blocks expect input

                    # this is just random text - I'm using an integer string because some of the AC blocks do int casting.
                    alert.send_keys('1111')
                    alert.dismiss()

            #except NoAlertPresentException:
            except WebDriverException:
                # no input prompt for this ActiveCode
                pass

        #time.sleep(5) # not sure if this is really necessary or not.
        allErrors = self.driver.find_elements_by_class_name("error")

        for e in allErrors:
            print "Error in ActiveCode block %s on page %s." % (e.get_attribute('id'), url[url.rindex('/')+1:])


### Example stuff

# # get a div
# div = driver.find_element_by_id("ch03_4")
#
# # get the first button within the div
# button = div.find_element_by_tag_name('button')
# if button.text == 'Run':
#     button.click()
#
# # get the pre element
# pre = div.find_element_by_id("ch03_4_pre")
#
#
# try:
#     WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.ID,"ch03_4_pre"),"Zuki"))
#     print pre.text
# except:
#     print "not there"
#
# #finally:
# #    driver.quit()
