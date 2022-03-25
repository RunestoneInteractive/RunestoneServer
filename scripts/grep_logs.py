#!/usr/bin/env python3

# Search through the logs on all running containers - by default search
# for ERROR entries in the log.  If a pattern is given on the CL search
# for that instead.
#
# Print out the matches the first time you see them, then create a hash
# keep track of the number of times this message is seen. At the end
# print out the top n messages.
#
# %%
import subprocess
import re
import hashlib
import sys

if len(sys.argv) > 1:
    match_pat = re.compile(sys.argv[1])
else:
    match_pat = re.compile(r"^.*\| ERROR")

# %%
mcount = {}
mess = {}


def check_all_servers(pat):
    for i in range(1, 7):
        print(f"Getting log from server{i}")
        with subprocess.Popen(
            f"""ssh server{i}.runestoneacademy.org "cd ~/Runestone/RunestoneServer/production && docker compose logs" """,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        ) as process:
            for line in process.stdout:
                dline = line.decode("utf8")
                if pat.search(dline):
                    hash = hashlib.md5(line).hexdigest()
                    mcount[hash] = mcount.get(hash, 0) + 1
                    if mcount[hash] == 1:
                        print(dline)
                    mess[hash] = dline


# %%
def print_top_n(mcount, mess, n=20):
    i = 0
    for k, v in sorted(mcount.items(), key=lambda x: x[1], reverse=True):
        print(v, mess[k].strip())
        i += 1
        if i > n:
            break


# %%
if __name__ == "__main__":
    check_all_servers(match_pat)
    print_top_n(mcount, mess)
