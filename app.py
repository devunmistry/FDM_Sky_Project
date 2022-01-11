from flask import Flask, request

from mysql_functions.mysql_function_create_router_object import create_router_object_mysql_connector
from mysql_functions.mysql_function_pull_one_router import pull_one_router_mysql_connector
from mysql_functions.mysql_function_change_router_dry_run import change_router_dry_run_mysql_connector

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

@app.route("/<num>/configure_loopback/", methods = ["POST"])
def app_configure_loopback(num):
    '''
    POST API: creates loopback interface for a given router
    :param num: router_id of router to be configured, references MYSQL primary key
    :param loopback_id: loopback to be added
    :param loopback_ip: ip address of loopback to be added
    :param loopback_subnet_mask: subnet mask of loopback to be added
    :returns: Completed/error string
    '''

    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])

    router_object_arguements = request.get_json()
    return router.configure_loopback(router_object_arguements["loopback_id"], router_object_arguements["loopback_ip"], router_object_arguements["loopback_subnet_mask"])

@app.route("/<num>/delete_loopback/", methods = ["DELETE"])
def app_delete_loopback(num):
    '''
    DELETE API: deletes given loopback interface for given router
    :param num: router_id of router to be configured, references MYSQL primary key
    :param loopback_id: loopback to be deleted
    :returns: Completed/error string
    '''

    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
    return router.delete_loopback(int(request.args["loopback_id"]))

@app.route("/<num>/list_interfaces/", methods = ["GET"])
def app_list_interfaces(num):
    '''
    GET API: gets all interfaces for given router
    :param num: router_id of router to be configured, references MYSQL primary key
    :returns: XML of all router interfaces
    '''

    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
    return router.list_interfaces()

@app.route("/<num>/change_dry_run/", methods = ["POST"])
def app_change_dry_run(num):
    '''
    POST API: flips dry_run setting for given router
    :param num: router_id of router to be configured, references MYSQL primary key
    :returns: Completed/error string
    '''

    router_data = pull_one_router_mysql_connector(num)[0]
    router = Router(router_data[1], router_data[2], router_data[3], router_data[4], router_data[5])
    
    router.change_dry_run()
    
    return change_router_dry_run_mysql_connector(num, router.dry_run)

if __name__ == "__main__":
    app.run()