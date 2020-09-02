import requests as rq
import logging

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

response.headers[
    "Access-Control-Allow-Headers"
] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, HEAD, OPTIONS"


# Using this function makes the runestone proxy act like a load balancer
# for using more than one jobe server.
#
def get_jobe_server():
    if settings.num_jobes:
        num_servers = settings.num_jobes
    else:
        num_servers = 1

    if auth.user:
        servernum = auth.user.id % (num_servers + 1)
        if servernum < num_servers:
            servernum = 0
        else:
            servernum = 1
    elif request.client:
        servernum = request.client.split(".")[-1]
        if servernum.isnumeric():
            servernum = int(servernum) % num_servers
    else:
        servernum = 0
    logger.debug(f"SERVER SELECTED = {servernum} for {request.client}")
    try:
        server = settings.jobe_server.format(servernum)
    except:
        server = settings.jobe_server

    return server


def jobeRun():
    req = rq.Session()
    logger.debug("got a jobe request %s", request.vars.run_spec)

    req.headers["Content-type"] = "application/json; charset=utf-8"
    req.headers["Accept"] = "application/json"
    if settings.jobe_key:
        req.headers["X-API-KEY"] = settings.jobe_key

    uri = "/jobe/index.php/restapi/runs/"
    url = get_jobe_server() + uri
    rs = {"run_spec": request.vars.run_spec}
    resp = req.post(url, json=rs)

    logger.debug("Got response from JOBE %s ", resp.status_code)
    return resp.content


def jobePushFile():
    req = rq.Session()
    logger.debug("got a jobe request %s", request.vars.run_spec)

    req.headers["Content-type"] = "application/json; charset=utf-8"
    req.headers["Accept"] = "application/json"
    req.headers["X-API-KEY"] = settings.jobe_key

    uri = "/jobe/index.php/restapi/files/" + request.args[0]
    url = get_jobe_server() + uri
    rs = {"file_contents": request.vars.file_contents}
    resp = req.put(url, json=rs)

    logger.debug("Got response from JOBE %s ", resp.status_code)

    response.status = resp.status_code
    return resp.content


def jobeCheckFile():
    req = rq.Session()
    logger.debug("got a jobe request %s", request.vars.run_spec)

    req.headers["Content-type"] = "application/json; charset=utf-8"
    req.headers["Accept"] = "application/json"
    req.headers["X-API-KEY"] = settings.jobe_key
    uri = "/jobe/index.php/restapi/files/" + request.args[0]
    url = get_jobe_server() + uri
    resp = req.head(url)
    logger.debug("Got response from JOBE %s ", resp.status_code)

    response.status = resp.status_code
    if resp.status_code == 404:
        response.status = 208

    return resp.content


def pytutor_trace():
    code = request.vars.code
    lang = request.vars.lang
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    if request.vars.stdin:
        stdin = request.vars.stdin
    else:
        stdin = ""

    url = f"http://tracer.runestone.academy:5000/trace{lang}"
    try:
        r = rq.post(url, data=dict(src=code, stdin=stdin), timeout=30)
    except rq.ReadTimeout:
        logger.error(
            "The request to the trace server timed out, you will need to rerun the build"
        )
        return ""
    if r.status_code == 200:
        if lang == "java":
            return r.text
        else:
            res = r.text[r.text.find('{"code":') :]
            return res
    logger.error(f"Unknown error occurred while getting trace {r.status_code}")
    return "Error in pytutor_trace"
