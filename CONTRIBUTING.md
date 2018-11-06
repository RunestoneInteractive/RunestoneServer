So you want to help with the development of the Runestone Server.  Thanks!

This document is meant to be a collection of things that will make that a bit easier.

# Installation
Installing all of the prerequisites needed to run your own server or help with development is covered extensively in the README, so I won't repeat that here.

# A Tour of the Source
The Runestone Server is built on top of the [web2py](http://web2py.com) application framework.  I know, you've never heard of web2py, why would I do such a thing?  In 2011 it seemed like the right choice.  If I were starting again today it would definitely be a [Flask](http://www.pocoo.org/flask) application.  I still hope to port everything to Flask one day.  But when I think about the opportunity cost of taking an entire summer to port the code versus using the summer to add new features to what is there, I lean heavily towards the new thing.  Eventually all of the bad decisions and shortcuts I've taken over the years will force me to do a rewrite.

Ok, with that out of the way, lets look at the structure of the source.  Web2py enforces a particular directory structure on your project and once you understand it, it is actually pretty nice.   The really important parts of the directory structure map directly to web2py's strictly enforced Model-View-Controller view of web development.   Here is an overview, with details to follow

    web2py/
        web2py.py
        applications/
            welcome/
            runestone/
                models/
                    0.py
                    1.py
                    db.py
                    db_ebook.py
                controllers/
                    ajax.py
                    default.py
                    admin.py
                views/
                    layout.html
                    index.html
                    generic.html
                    generic.json
                    default/
                        about.html
                        profile.html
                    admin/
                        showassignments.html
                errors/
                databases/

The web2py.py application folder is what you get when you download web2py from web2py.com.  All web2py applications have their own folder inside the web2py applications folder.  Out of the box, web2py comes with a welcome app, and this is where you clone the RunestoneServer repository to the the runestone folder.

Three critical folders inside runestone are the models, views, and controllers folders.  The models folder is where you write your table definitions for any database tables you are using in your application.  The files in the model folder are loaded in alphabetical order, so if you have some tables that depend on others you can control the order they are loaded by naming the files appropriately. Importantly, 0.py and 1.py are loaded right away and typically contain configuration information.  There is also a `databases` folder where web2py keeps track of meta information about each table.  it uses this to detect when you have made a schema change and will automatically do its best to update the tables in the database and migrate any data to the new schema.  You should never edit any of these files, or you will cause more trouble than its worth.

The controllers folder contains all of the endpoints for making application requests.  Routing is done by a simple naming convention as follows:  `/application/controller_file/function`. So a request to /`runestone/ajax/hsblog` would cause the hsblog function defined inside ajax.py in the controllers folder to be called.  For runestone all of the API calls used by the Javascript make calls to functions inside of ajax.py.

Every controller file may have a folder with the same name under the views folder.  Each function in a controller may have a corresponding html file inside said folder.  An example:  Suppose you have a controller `/runestone/admin/listcourses` The list courses function would get all of the database information needed to list all of the courses and store that information in a python dictionary.  The listcourses function returns that dictionary, and web2py marries that information with the template file in `/runestone/views/admin/listcourses.html`. The only time your would not have a corresponding html file is when your controller is meant to return JSON or XML.  In this case you should make the request to `/runestone/ajax/foo.json`. This will ensure that the foo function in ajax is called, and the .json extension lets web2py know to set up the content-type headers to indicate that it is JSON coming back.  If you do not have an html file in your view folder web2py will default to `generic.html` file in the main views folder.  This actually works fine when you are prototyping as web2py does a decent job of trying to display whatever stuff you send it in a dictionary.

Generally the  web2py templating system is a lot like Jinja2, but with a couple of syntactic differences to get used to.  For example whereas in Jinja you can reference a variable like `{{foo}}` in web2py you need to say `{{=foo}}`

## More about web2py

Generally the web2py documentation is pretty good, if you are confused after looking at our code you can check out either of the links below.  It might also be a good idea to just work through your own really [simple examples](http://www.web2py.com/init/default/examples).  For more reference style documentation check out either of the following:

* [web2py.readthedocs.io](http://web2py.readthedocs.org)
* [www.web2py.com/book](http://www.web2py.com/book)

## Unit Testing

We have a small set of unit tests that we really want to grow into a full blown full coverage set of tests.  To run the unit tests you will need to `pip install -U -r requirements-test.txt`, `cd tests`, then run the `run_tests.py` script. You should also set your `TEST_DBURL` environment variable to connect to the runestone_test database.

We have a Travis-CI job set up to automatically test all PR's if your pull request does not pass it won't be accepted.

Please take a look at the few unit tests we have, and write a new one that demonstrates that your feature or enhancement works.

## Major Feature Contributions

There are many ways that we can continue to improve and make the Runestone platform great, and I am exctied to see the platform evolve.  What I would ask is that if you have a large new feature that you would like to propose / contribute please start by creating an issue.  This will allow us to discuss it together up front, consider the design implications, and make it more likely that the PR will be accepted with a minimum of fuss.

Runestone has grown organically over the years but that has led to duplicated tables in the database duplicated code and lots of inconsistency.  We need to start working to change all of that if we are going to continue to grow runestone efficiently.

