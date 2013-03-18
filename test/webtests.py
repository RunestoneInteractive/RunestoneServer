from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# go to a page by URL
driver.get("http://127.0.0.1:8000/runestone/static/thinkcspy/PythonTurtle/helloturtle.html")

# get a div
div = driver.find_element_by_id("ch03_4")

# get the first button within the div
button = div.find_element_by_tag_name('button')
if button.text == 'Run':
    button.click()

# get the pre element
pre = div.find_element_by_id("ch03_4_pre")


try:
    WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.ID,"ch03_4_pre"),"Zuki"))
    print pre.text
except:
    print "not there"

#finally:
#    driver.quit()


done = False

while not done:
    allButtons = driver.find_elements_by_tag_name("button")

    for button in allButtons:
        if button.text == "Run":
            button.click()

    time.sleep(5) # not sure if this is really necessary or not.
    allErrors = driver.find_elements_by_class_name("error")

    for e in allErrors:
        print "There was an error in div %s " % e.get_attribute("id")

    lnext = driver.find_element_by_link_text("next")
    if lnext:
        print "going to: %s" % lnext.get_attribute("href")
        lnext.click()
    else:
        done = True


# find the element that's name attribute is q (the google search box)
#inputElement = driver.find_element_by_name("q")

# type in the search
#inputElement.send_keys("Cheese!")

# submit the form (although google automatically searches now without submitting)
#inputElement.submit()

# the page is ajaxy so the title is originally this:
#print driver.title
#driver.find_element_by_id("")
# try:
#     # we have to wait for the page to refresh, the last thing that seems to be updated is the title
#     WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
#
#     # You should see "cheese! - Google Search"
#     print driver.title
#
# finally:
#     driver.quit()

#driver.quit()


# div.find_elements_by_tag_name("input")  # returns a list of input elements. maybe checkboxes for example
