from flask import Flask
from flask_cors import CORS
from routes.api.api_routes import api_routes
from routes.webapp.web_routes import webapp_blueprint
import subprocess
import threading


class Server:
    def __init__(self, build_dir: str, port: int=8000):
        self.app = Flask(__name__, static_url_path='', static_folder=build_dir)
        CORS(self.app)

        self.app.register_blueprint(webapp_blueprint)
        self.app.register_blueprint(api_routes)

        self.port = port

    def run(self):
        self.app.run(use_reloader=True, port=self.port, threaded=True, debug=True)


def start_ipfs_daemon():
    ipfs_local = "ipfs"
    subprocess.run([ipfs_local, "daemon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
    build_dir = "../WebApp/build"
    ipfs_thread = threading.Thread(target=start_ipfs_daemon)
    ipfs_thread.start()
    my_app = Server(build_dir)
    my_app.run()
