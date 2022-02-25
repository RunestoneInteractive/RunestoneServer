import re
import sys

# 104.255.205.41 - [22/Feb/2022:19:25:46 +0000] Request: "POST /runestone/proxy/jobeRun HTTP/1.1" Status: 200 Bytes: 242 Host: 10.136.0.8:80  ResponseTime: 4.204 Referrer: "https://runestone.academy/runestone/assignments/doAssignment?assignment_id=97720" Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
if len(sys.argv) > 1:
    logfile = open(sys.argv[1], "r")
else:
    logfile = sys.stdin

print(
    "IPRequest,timestamp,Request,Status,Bytes,HostAssigned,ResponseTime,ReferringPage,Agent"
)
for line in logfile:
    if g := re.match(
        r"^(.*) - \[(.*?)\] Request: (.*?) Status: (\d+) Bytes: (\d+) Host: (.*?) ResponseTime: (.*?) Referrer: (.*?) Agent: (.*?)$",
        line,
    ):
        print(
            f"{g.group(1)},{g.group(2)},{g.group(3)},{g.group(4)},{g.group(5)},{g.group(6)},{g.group(7)},{g.group(8)},{g.group(9)}"
        )
