__author__ = 'isaacdontjelindell'

from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
import time


##### IMPORTANT! ##################################################

# You must download the ChromeDriver version appropriate for your
# platform and Chrome version. (You can find the download page at:
# https://code.google.com/p/chromedriver/downloads/list.

# Put the binary in this directory and update the filename param:
chromedriver_filename = "chromedriver.v27-v30.linux-amd64"

###################################################################

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(chromedriver_filename)
host = 'http://127.0.0.1:8000'


def testActiveCodeForPage():
    allButtons = driver.find_elements_by_tag_name("button")

    for button in allButtons:
        try:
            if button.text == "Run":
                button.click()
        except UnexpectedAlertPresentException: # some of the ActiveCodes expect input
            alert = driver.switch_to_alert()

            # this is some random text - I'm using an integer string because some of the AC blocks do int casting.
            alert.send_keys('50')
            alert.dismiss()
        except Exception, e:
            print "there was an error clicking:"
            print e
            print ""

    time.sleep(5) # not sure if this is really necessary or not.
    name = driver.find_elements_by_class_name("error")
    allErrors = name

    for e in allErrors:
        print "There was an error in div %s " % e.get_attribute("id")
        print ""


# Get the master list for thinkcspy
driver.get(host + "/runestone/static/thinkcspy/toc.html")

chapters = driver.find_elements_by_class_name('toctree-l1')
link_list = []
for c in chapters:
    l = c.find_element_by_tag_name('a')
    link_list.append(l.get_attribute('href'))

for l in link_list:
    driver.get(l)
    print "Testing activecode blocks on page: ", l[l.rindex('/')+1:]
    testActiveCodeForPage()

driver.quit()


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
