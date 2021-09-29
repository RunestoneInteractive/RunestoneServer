# *******************************************************************************
# |docname| - Provide a web-based GUI for configuring and invoking a Docker build
# *******************************************************************************

from click_web import create_click_web_app
import docker_tools

app = create_click_web_app(docker_tools, docker_tools.install)

if __name__ == "__main__":
    app.run()
