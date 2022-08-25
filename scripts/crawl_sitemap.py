import sys
import logging
from pysitemap import crawler

# this script crawls the site and makes a sitemap.xml file.
# I think it is better/faster to use the other script that walks the file system
# and includes everything under published/XXX

if __name__ == "__main__":
    if "--iocp" in sys.argv:
        from asyncio import events, windows_events

        sys.argv.remove("--iocp")
        logging.info("using iocp")
        el = windows_events.ProactorEventLoop()
        events.set_event_loop(el)

    # root_url = sys.argv[1]
    root_url = "https://runestone.academy"
    crawler(
        root_url,
        out_file="sitemap.xml",
        exclude_urls=[".pdf", ".jpg", ".png", ".zip", "reportabug"],
    )
