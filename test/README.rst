Testing with Selenium
=====================


Selenium  (docs.seleniumhq.org)  provides some tools for automatically driving your web pages and doing some testing.  With a site that is continually under development its important to have some automated regression tests.  Selenium lets us write these tests and in runs them in a real browser.

Use ``pip`` to install selenium.

Here's an example of a simple first program for running every activecode block in the book.  It runs the activecodes and then checks to see if any of the runs fail by looing for elements with class equal to error.

.. sourcecode:: python

   from selenium import webdriver
   from selenium.webdriver.common.by import By
   from selenium.common.exceptions import TimeoutException
   from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
   from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

   # Create a new instance of the Firefox driver
   driver = webdriver.Firefox()

   # go to a page by URL
   driver.get("http://127.0.0.1:8000/runestone/static/thinkcspy/PythonTurtle/helloturtle.html")

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


