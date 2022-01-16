from flask import Flask, request

from mysql_functions.mysql_function_create_router_object import create_router_object_mysql_connector
from mysql_functions.mysql_function_pull_one_router import pull_one_router_mysql_connector

from sky_project import Router

app = Flask(__name__)

@app.route("/create_router_object/", methods = ["POST"])
def app_create_router_object():
    '''
    POST API: creates router entry in MYSQL
    :param router_object_arguements: json file containing host, port, username, password for router to be added
    :returns: Completed/error string
    '''

    router_object_arguements = request.get_json()
    return create_router_object_mysql_connector(router_object_arguements["host"], router_object_arguements["port"], router_object_arguements["username"], router_object_arguements["password"])

@app.route("/<num>/configure_loopback/", methods = ["POST", "PUT"])
def app_configure_loopback(num):
    '''
    POST API: creates loopback interface for a given router
    :param num: router_id of router to be configured, references MYSQL primary key
    :param dry_run: Boolean. If True, returns payload to user. Otherwise connects to router.
    :param loopback_id: loopback to be added
    :param loopback_ip: ip address of loopback to be added
    :param loopback_subnet_mask: subnet mask of loopback to be added
    :returns: Completed/error string
    '''

    #Get router data
    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4])
    
    #Get interface data
    interface_config_data = request.get_json()
    dry_run = eval(interface_config_data["dry_run"])
    loopback_id = interface_config_data["loopback_id"]
    loopback_ip = interface_config_data["loopback_ip"]
    loopback_subnet_mask = interface_config_data["loopback_subnet_mask"]

    #Get the current config to pull data, if the interface is going to be configured
    if dry_run == False:
        current_config = app_list_interfaces(num)
    
    if request.method == "POST":
        if "<loopback>%s</loopback>" % (loopback_id) in current_config:
            return "Invalid: loopback id already configured"
        else:
            return router.configure_loopback(dry_run, loopback_id, loopback_ip, loopback_subnet_mask)
    
    if request.method == "PUT":
        if "<loopback>%s</loopback>" % (loopback_id) not in current_config:
            return "Invalid: loopback id not currently configured"
        else:
            return router.configure_loopback(dry_run, loopback_id, loopback_ip, loopback_subnet_mask)

@app.route("/<num>/delete_loopback/", methods = ["DELETE"])
def app_delete_loopback(num):
    '''
    DELETE API: deletes given loopback interface for given router
    :param num: router_id of router to be configured, references MYSQL primary key
    :param dry_run: Boolean. If True, returns payload to user. Otherwise connects to router.
    :param loopback_id: loopback to be deleted
    :returns: Completed/error string
    '''

    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4])
    return router.delete_loopback(eval(request.args["dry_run"]), int(request.args["loopback_id"]))

@app.route("/<num>/list_interfaces/", methods = ["GET"])
def app_list_interfaces(num):
    '''
    GET API: gets all interfaces for given router
    :param num: router_id of router to be configured, references MYSQL primary key
    :param dry_run: Boolean. If True, returns payload to user. Otherwise connects to router.
    :returns: XML of all router interfaces
    '''

    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4])
    return router.list_interfaces(eval(request.args["dry_run"]))

if __name__ == "__main__":
    app.run()