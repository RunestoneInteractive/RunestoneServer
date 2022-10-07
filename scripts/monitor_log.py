import time

# import subprocess
# import select
#
# f = subprocess.Popen(['tail','-F',filename],\
#         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# p = select.poll()
# p.register(f.stdout)
#
# while True:
#     if p.poll(1):
#         print f.stdout.readline()
#     time.sleep(1)
#
#
import os, sys, time
import re
from dateutil.parser import parse
import datetime
import pdb
from pytz import timezone

cst = timezone("America/Chicago")
timepat = re.compile(
    r".*/(dashboard|proxy|assignments|logger|assessment|books)/(\w+)(\s*|/.*?|\?.*?|\.html.*?) HTTP.*ResponseTime: (\d+\.\d+)"
)
datepat = re.compile(
    r".*\[(\d+/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d\d\d\d):(.*?)\].*"
)
statuspat = re.compile(r".*Status:\s+(\d+)\s+.*")
hostpat = re.compile(r".*Host:\s+(\d+\.\d+\.\d+\.\d+:\d+)\s+.*")

name = "/var/log/nginx/access.log"


# Table mapping response codes to messages; entries have the
# form {code: (shortmessage, longmessage)}.
responses = {
    100: ("Continue", "Request received, please continue"),
    101: ("Switching Protocols", "Switching to new protocol; obey Upgrade header"),
    200: ("OK", "Request fulfilled, document follows"),
    201: ("Created", "Document created, URL follows"),
    202: ("Accepted", "Request accepted, processing continues off-line"),
    203: ("Non-Authoritative Information", "Request fulfilled from cache"),
    204: ("No Content", "Request fulfilled, nothing follows"),
    205: ("Reset Content", "Clear input form for further input."),
    206: ("Partial Content", "Partial content follows."),
    300: ("Multiple Choices", "Object has several resources -- see URI list"),
    301: ("Moved Permanently", "Object moved permanently -- see URI list"),
    302: ("Found", "Object moved temporarily -- see URI list"),
    303: ("See Other", "Object moved -- see Method and URL list"),
    304: ("Not Modified", "Document has not changed since given time"),
    305: (
        "Use Proxy",
        "You must use proxy specified in Location to access this " "resource.",
    ),
    307: ("Temporary Redirect", "Object moved temporarily -- see URI list"),
    400: ("Bad Request", "Bad request syntax or unsupported method"),
    401: ("Unauthorized", "No permission -- see authorization schemes"),
    402: ("Payment Required", "No payment -- see charging schemes"),
    403: ("Forbidden", "Request forbidden -- authorization will not help"),
    404: ("Not Found", "Nothing matches the given URI"),
    405: ("Method Not Allowed", "Specified method is invalid for this server."),
    406: ("Not Acceptable", "URI not available in preferred format."),
    407: (
        "Proxy Authentication Required",
        "You must authenticate with " "this proxy before proceeding.",
    ),
    408: ("Request Timeout", "Request timed out; try again later."),
    409: ("Conflict", "Request conflict."),
    410: ("Gone", "URI no longer exists and has been permanently removed."),
    411: ("Length Required", "Client must specify Content-Length."),
    412: ("Precondition Failed", "Precondition in headers is false."),
    413: ("Request Entity Too Large", "Entity is too large."),
    414: ("Request-URI Too Long", "URI is too long."),
    415: ("Unsupported Media Type", "Entity body in unsupported format."),
    416: ("Requested Range Not Satisfiable", "Cannot satisfy request range."),
    417: ("Expectation Failed", "Expect condition could not be satisfied."),
    500: ("Internal Server Error", "Server got itself in trouble"),
    501: ("Not Implemented", "Server does not support this operation"),
    502: ("Bad Gateway", "Invalid responses from another server/proxy."),
    503: (
        "Service Unavailable",
        "The server cannot process the request due to a high load",
    ),
    504: ("Gateway Timeout", "The gateway server did not receive a timely response"),
    505: ("HTTP Version Not Supported", "Cannot fulfill request."),
}


def output_stats(the_bin, bin_num):
    with open("/home/bmiller/response_codes.txt", "w") as f:
        f.write(f"Time = {datetime.datetime.now(cst)}\n")
        f.write("-----\n")
        for k, v in sorted(the_bin.items()):
            f.write(f'{k} {v:>6} {responses.get(int(k), ("", ""))[0]}\n')


current = open(name, "r")
curino = os.fstat(current.fileno()).st_ino
stats = {i: {} for i in range(12)}
current_bin = 0

while True:
    while True:
        line = current.readline()
        if line == "":
            break
        if gd := datepat.match(line):
            current_time = parse(gd.group(1) + " " + gd.group(3))
            bin = int(current_time.minute / 60 * 12)
            if bin != current_bin:
                # print(current_time, gd.group(1), gd.group(3))
                output_stats(stats[current_bin], current_bin)
                stats[current_bin] = {}
                current_bin = bin
            if gd := statuspat.match(line):
                status = gd.group(1)
                stats[bin][status] = stats[bin].get(status, 0) + 1
            # sys.stdout.write(str(currentday))
    try:
        if os.stat(name).st_ino != curino:
            new = open(name, "r")
            current.close()
            current = new
            curino = os.fstat(current.fileno()).st_ino
            continue
    except IOError:
        pass
    time.sleep(1)
