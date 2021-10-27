#!/usr/bin/env python3
#
# ****************************************************************
# |docname| - Provide a web-based GUI for running the Docker tools
# ****************************************************************

from click_web import create_click_web_app
import docker_tools

app = create_click_web_app(docker_tools, docker_tools.cli)

if __name__ == "__main__":
    app.run()
