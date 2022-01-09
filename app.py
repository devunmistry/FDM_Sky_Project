from flask import Flask, request, templating, url_for

from mysql_connector import mysql_add_router, mysql_pull_all_routers, mysql_pull_one_router, mysql_change_router_dry_run
from sky_project import Router

app = Flask(__name__)

@app.route("/")
def app_home():
    router_all_data = mysql_pull_all_routers()
    return templating.render_template("home.html", router_all_data = router_all_data)

@app.route("/create_router_object/")
def app_create_router_object():
    return mysql_add_router(request.args["ip_address"], request.args["port"], request.args["username"], request.args["password"])

@app.route("/<num>/", methods = ["GET", "POST"])
def app_router_home(num):
    return templating.render_template("router_home.html")

@app.route("/<num>/configure_loopback/")
def app_configure_loopback(num):
    if request.method == "GET":
        router_data = mysql_pull_one_router(num)[0]
        router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
        return router.configure_loopback(int(request.args["loopback_id"]), request.args["loopback_ip"], request.args["loopback_subnet_mask"])
    else:
        return url_for("router_home")

@app.route("/<num>/delete_loopback/")
def app_delete_loopback(num):
    if request.method == "GET":
        router_data = mysql_pull_one_router(num)[0]
        router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
        return router.delete_loopback(int(request.args["loopback_id"]))
    else:
        return url_for("router_home")

@app.route("/<num>/list_interfaces/", methods = ["GET", "POST"])
def app_list_interfaces(num):
    router_data = mysql_pull_one_router(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
    return router.list_interfaces()

@app.route("/<num>/change_dry_run/", methods = ["GET", "POST"])
def app_change_dry_run(num):
    router_data = mysql_pull_one_router(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
    
    router.dry_run = abs(router.dry_run - 1)
    
    return mysql_change_router_dry_run(num, router.dry_run)

if __name__ == "__main__":
    app.run()