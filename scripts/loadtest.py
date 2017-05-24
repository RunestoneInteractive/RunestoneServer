from locust import HttpLocust, TaskSet, task

class SimpleTests(TaskSet):

    @task
    def index(self):
        self.client.get("/", verify=False)
    
    @task
    def home(self):
        self.client.get("/runestone/static/thinkcspy/index.html", verify=False)

    @task
    def logrun(self):
        self.client.post("/runestone/ajax/hsblog", 
            {'event': 'activecode', 'act': 'edit', 'div_id': 'logtest'},
            verify=False)

class WebsiteUser(HttpLocust):
    task_set = SimpleTests
    min_wait = 5000
    max_wait = 15000

