from flask import Flask, request, templating, url_for
from sky_project import Router

app = Flask(__name__)

router_a = Router("192.168.0.101", 830, "cisco", "cisco")

@app.route("/router_home/", methods = ["GET", "POST"])
def app_router_home():
    return templating.render_template("router_home.html")

@app.route("/configure_loopback/", methods = ["GET", "POST"])
def app_configure_loopback():
    if request.method == "POST":
        return router_a.configure_loopback(int(request.form["loopback_id"]), request.form["loopback_ip"], request.form["loopback_subnet_mask"])
    else:
        return url_for("router_home")

@app.route("/delete_loopback/", methods = ["GET", "POST"])
def app_delete_loopback():
    if request.method == "POST":
        loopback_id = int(request.form["loopback_id"])
        return router_a.delete_loopback(loopback_id)
    else:
        return url_for("router_home")

@app.route("/list_interfaces/", methods = ["GET", "POST"])
def app_list_interfaces():
    return router_a.list_interfaces()

@app.route("/change_dry_run/", methods = ["GET", "POST"])
def app_change_dry_run():
    return router_a.change_dry_run()

if __name__ == "__main__":
    app.run()