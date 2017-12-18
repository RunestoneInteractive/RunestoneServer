import requests as rq
import logging
import json
logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

response.headers["Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
response.headers["Access-Control-Allow-Methods"] = 'GET, PUT, POST, HEAD, OPTIONS'

def jobeRun():
    req = rq.Session()
    logger.debug("got a jobe request %s", request.vars.run_spec)

    req.headers['Content-type'] = 'application/json; charset=utf-8'
    req.headers['Accept'] = 'application/json'
    req.headers['X-API-KEY'] = settings.jobe_key
    
    uri = '/jobe/index.php/restapi/runs/'
    url = settings.jobe_server + uri
    rs = {'run_spec': request.vars.run_spec}
    resp = req.post(url, json=rs)

    logger.debug("Got response from JOBE %s ", resp.status_code)
    return resp.content

def jobePushFile():
    req = rq.Session()
    logger.debug("got a jobe request %s", request.vars.run_spec)

    req.headers['Content-type'] = 'application/json; charset=utf-8'
    req.headers['Accept'] = 'application/json'
    req.headers['X-API-KEY'] = settings.jobe_key

    uri = '/jobe/index.php/restapi/files/'+request.args[0]
    url = settings.jobe_server + uri
    rs = {'file_contents': request.vars.file_contents}
    resp = req.put(url, json=rs)

    logger.debug("Got response from JOBE %s ", resp.status_code)
    
    response.status = resp.status_code
    return resp.content

def jobeCheckFile():
    req = rq.Session()
    logger.debug("got a jobe request %s", request.vars.run_spec)

    req.headers['Content-type'] = 'application/json; charset=utf-8'
    req.headers['Accept'] = 'application/json'
    req.headers['X-API-KEY'] = settings.jobe_key
    uri = '/jobe/index.php/restapi/files/'+request.args[0]
    url = settings.jobe_server + uri
    rs = {'file_contents': request.vars.file_contents}
    resp = req.head(url)
    logger.debug("Got response from JOBE %s ", resp.status_code)

    response.status = resp.status_code
    if resp.status_code == 404:
        response.status = 208
    
    return resp.content

