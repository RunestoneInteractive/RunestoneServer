import requests as rq
import logging

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

response.headers[
    "Access-Control-Allow-Headers"
] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, HEAD, OPTIONS"


def jobeRun():
    req = rq.Session()
    logger.debug("got a jobe request %s", request.vars.run_spec)

    req.headers["Content-type"] = "application/json; charset=utf-8"
    req.headers["Accept"] = "application/json"
    if settings.jobe_key:
        req.headers["X-API-KEY"] = settings.jobe_key

    uri = "/jobe/index.php/restapi/runs/"
    url = settings.jobe_server + uri
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
    url = settings.jobe_server + uri
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
    url = settings.jobe_server + uri
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
