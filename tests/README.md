# Testing Runestone


## Unit Tests

```
python run_tests.py
```

Or if you have a docker container set up:

```
docker exec -it runestoneserver_runestone_1 bash -c 'cd applications/runestone/tests; python run_tests.py'
```

## Load Tests

From the scripts folder, run the command:

```
locust -f locustfile.py
```

Then in your browser go to `http://127.0.0.1:8089` You an set up how many users you want and how fast they will come online.  The webpage will update every couple of seconds to show you statistics on load times for various kinds of pages.

