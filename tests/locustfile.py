from locust import HttpLocust, TaskSet, task
import bs4
import random
import sys, os

class WebsiteTasks(TaskSet):
    def on_start(self):
        res = self.client.get("/runestone/default/user/login")
        pq = bs4.BeautifulSoup(res.content, features='lxml')
        # Get the csrf key for successful submission
        i = pq.select('input[name="_formkey"]')
        token = i[0]['value']
        # login a user
        try:
            user = os.environ['RUNESTONE_TESTUSER']
            pw = os.environ['RUNESTONE_TESTPW']
        except:
            print("ERROR please set RUNESTONE_TESTUSER and RUNESTONE_TESTPW ")
            sys.exit(-1)
        res = self.client.post("/runestone/default/user/login",
        {"username": user,
        "password": pw,
        "_formkey": token,
        "_formname": 'login'})
        # Get the index and make a list of all chapters/subchapters
        res = self.client.get("/runestone/books/published/fopp/index.html")
        pq = bs4.BeautifulSoup(res.content, features='lxml')
        pages = pq.select('.toctree-l2 a')
        self.bookpages = [p['href'] for p in pages]

    @task(5)
    def index(self):
        self.client.get("/runestone")

    @task(20)
    def boookpage(self):
        # pick a page at random
        url = random.choice(self.bookpages)
        base = '/runestone/books/published/fopp/'
        res = self.client.get(base + url)
        pq = bs4.BeautifulSoup(res.content, features='lxml')
        # client.get ONLY gets the html, so we need to simulate getting all
        # of the static assets ourselves.
        for s in pq.select('script'):
            if s.has_attr('src'):
                if s['src'].startswith(("http","//")) == False:
                    js = self.client.get(base + s['src'].replace('../',''), name="scripts")
        for s in pq.select('link'):
            if s.has_attr('href'):
                if s['href'].startswith(("http","//")) == False:
                    css = self.client.get(base + s['href'].replace('../',''), name='css')

class WebsiteUser(HttpLocust):
    host='http://localhost'
    task_set = WebsiteTasks
    min_wait = 1000
    max_wait = 15000