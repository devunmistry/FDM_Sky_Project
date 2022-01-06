from flask import Flask
from sky_project import Router

app = Flask(__name__)

@app.route("/configure_loopback/", methods = ["GET", "POST"])
def API_configure_loopback():
    router = Router("192.168.0.101", 830, "cisco", "cisco")
    return router.configure_loopback(1, "192.168.1.1", "255.255.255.0")

@app.route("/delete_loopback/", methods = ["GET", "POST"])
def API_delete_loopback():
    router = Router("192.168.0.101", 830, "cisco", "cisco")
    return router.delete_loopback(1)

@app.route("/list_interfaces/", methods = ["GET", "POST"])
def API_list_interfaces():
    router = Router("192.168.0.101", 830, "cisco", "cisco")
    return router.list_interfaces()

if __name__ == "__main__":
    app.run()