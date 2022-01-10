from flask import Flask, request, templating, url_for

from mysql_functions.mysql_function_add_router import add_router_mysql_connector
from mysql_functions.mysql_function_pull_all_routers import pull_all_routers_mysql_connector
from mysql_functions.mysql_function_pull_one_router import pull_one_router_mysql_connector
from mysql_functions.mysql_function_change_router_dry_run import change_router_dry_run_mysql_connector

from sky_project import Router

app = Flask(__name__)

@app.route("/")
def app_home():
    router_all_data = pull_all_routers_mysql_connector()
    return templating.render_template("home.html", router_all_data = router_all_data)

@app.route("/create_router_object/")
def app_create_router_object():
    return add_router_mysql_connector(request.args["ip_address"], request.args["port"], request.args["username"], request.args["password"])

@app.route("/<num>/", methods = ["GET", "POST"])
def app_router_home(num):
    return templating.render_template("router_home.html")

@app.route("/<num>/configure_loopback/")
def app_configure_loopback(num):
    if request.method == "GET":
        router_data = pull_one_router_mysql_connector(num)[0]
        router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
        return router.configure_loopback(int(request.args["loopback_id"]), request.args["loopback_ip"], request.args["loopback_subnet_mask"])
    else:
        return url_for("router_home")

@app.route("/<num>/delete_loopback/")
def app_delete_loopback(num):
    if request.method == "GET":
        router_data = pull_one_router_mysql_connector(num)[0]
        router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
        return router.delete_loopback(int(request.args["loopback_id"]))
    else:
        return url_for("router_home")

@app.route("/<num>/list_interfaces/", methods = ["GET", "POST"])
def app_list_interfaces(num):
    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
    return router.list_interfaces()

@app.route("/<num>/change_dry_run/", methods = ["GET", "POST"])
def app_change_dry_run(num):
    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
    
    router.change_dry_run()
    
    return change_router_dry_run_mysql_connector(num, router.dry_run)

if __name__ == "__main__":
    app.run()