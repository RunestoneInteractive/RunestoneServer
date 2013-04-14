from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
# Create a new instance of the Firefox driver
driver = webdriver.Firefox()
host = 'http://127.0.0.1:8000'


def testActiveCodeForPage():
    allButtons = driver.find_elements_by_tag_name("button")

    for button in allButtons:
        try:
            if button.text == "Run":
                button.click()
        except:
            print "there was an error clicking"

    time.sleep(5) # not sure if this is really necessary or not.
    allErrors = driver.find_elements_by_class_name("error")

    for e in allErrors:
        print "There was an error in div %s " % e.get_attribute("id")


# Get the master list
driver.get(host + "/runestone/static/thinkcspy/toc.html")

chapters = driver.find_elements_by_class_name('toctree-l1')
link_list = []
for c in chapters:
    l = c.find_element_by_tag_name('a')
    link_list.append(l.get_attribute('href'))

driver.get(host + "/runestone/static/pythonds/index.html")
chapters = driver.find_elements_by_class_name('toctree-l1')
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

