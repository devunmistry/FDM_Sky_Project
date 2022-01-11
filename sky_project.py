from functools import wraps
from ipaddress import ip_address
from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SSHError
from ncclient.operations.rpc import RPCError
from xml.dom.minidom import parseString

from xml_functions.xml_function_configure_loopback import configure_loopback_xml_renderer
from xml_functions.xml_function_delete_loopback import delete_loopback_xml_renderer
from xml_functions.xml_function_list_interfaces import list_interfaces_xml_renderer

class Router():

    def __init__(self, host, port, username, password, dry_run):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dry_run = dry_run

    ####################
    ## Decorators     ##
    ####################

    def _check_arguements_decorator(func):
        '''
        Decorator. Tests the router host and port are of the correct format. Also tests if given arguements (if applicable) are of the same format. Should be called before Class functions.
        :param func: function to be wrapped within decorator.
        :return: test_host_port_decorator_wrapper
        '''

        @wraps(func)
        def check_arguements_decorator_wrapper(self, *args):
            '''
            Decorator wrapper. Includes try/except for router host, and if statement for router port. Also includes if statement for interface_id and try/except for interface_ip and interface_subnet_mask, which are called if applicable
            :param self: self
            :param *args: arguements to be passed to wrapped function
            :return: func(*args)
            '''

            #check router socket ip address is of valid format
            try:
                ip_address(self.host)
            except(ValueError) as e:
                return "%s: Invalid ip address for router socket" % (e.__class__)

            #check router socket port is of valid format
            if type(self.port) is not int or self.port < 1 or self.port > 65535:
                return "Invalid port for router socket"

            try:
                loopback_id = args[0]
                if type(loopback_id) is not int or loopback_id < 0 or loopback_id > 2147483647:
                    return "Invalid id for loopback interface"
            except IndexError:
                pass

            try:
                loopback_ip = args[1]
                try:
                    ip_address(loopback_ip)
                except(ValueError) as e:
                    return "%s: Invalid ip address for loopback interface" % (e.__class__)
            except IndexError:
                pass

            try:
                loopback_subnet_mask = args[2]
                try:
                    ip_address(loopback_subnet_mask)
                except(ValueError) as e:
                    return "%s: Invalid subnet mask for loopback interface" % (e.__class__)
            except:
                pass
            
            return func(self, *args)
        
        return check_arguements_decorator_wrapper

    def _connect_ssh_decorator(self, xml_config):
        '''Decorator. Allows for xml_config to be returned to user if dry_run == 1. Should be called within Class functions.
        :param self: self
        :param xml_config: xml_config string to be sent to router, or returned to user if dry_run == 1
        :returns: connect_ssh_decorator_inner
        '''

        def connect_ssh_decorator_inner(func):
            '''
            Decorator inner function. Opens ssh connection with router. 
            :param self: self
            :param func: function to be wrapped within decorator
            :return: connect_ssh_decorator_wrapper
            '''

            def connect_ssh_decorator_wrapper(*args):
                '''
                Decorator wrapper. Calls ncclient.manager.connect_ssh to open ssh connection with router
                :param conf: xml configuration to be sent to router, or returned to user if dry_run == 1
                :param *args: arguements to be passed to wrapped function
                :return: func(*args, m)
                        m is ncclient.manager.connect_ssh
                '''

                #check if dry_run == 1 and return conf accordingly
                if self.dry_run == 1:
                    return xml_config

                #establish connection with router
                try:
                    with manager.connect_ssh(
                        host = self.host,
                        port = self.port,
                        username = self.username,
                        password = self.password,
                        hostkey_verify = False,
                        device_params = {"name":"csr"}) as m:
                            #run function within manager.connect_ssh
                            return func(*args, m)
                except (SSHError) as e:
                    return "%s: Could not open router socket %s:%s - could be incorrect ip address and/or port number" % (e.__class__, self.host, self.port)
                except (AuthenticationError) as e:
                    return "%s: Incorrect router SSH username and/or password" % (e.__class__)

            return connect_ssh_decorator_wrapper

        return connect_ssh_decorator_inner

    ####################
    ## Getters & setters ##
    ####################

    def change_dry_run(self):
        self.dry_run = abs(self.dry_run - 1)
        if self.dry_run == 0:
            return "dry_run = 0: Payload will be sent to router"
        if self.dry_run == 1:
            return "dry_run = 1: Payload will be returned to user"

    ####################
    ## Methods        ##
    ####################

    @_check_arguements_decorator
    def configure_loopback(self, loopback_id, loopback_ip, loopback_subnet_mask):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :param loopback_id: id number for the loopback being configured
        :param loopback_ip: ip address for the loopback being configured
        :param loopback_subnet_mask: subnet mask for the loopback being configured
        :return: configure_loopback_call_edit_config(), which calls m.edit_config(target = "running", config = conf, default_operation = "merge")
        '''

        conf = configure_loopback_xml_renderer(loopback_id, loopback_ip, loopback_subnet_mask)

        # define function calling edit config, to be run if above tests pass. Decorator opens ssh connection, or returns conf
        @self._connect_ssh_decorator(conf)
        def configure_loopback_call_edit_config(m):
            '''
            Calls edit config with parameters to create/edit a loopback interface
            :param m: ncclient.manager.connect_ssh as m, passed through by decorator
            :return: m.edit_config(target = "running", config = conf, default_operation = "merge")
            '''
            try:
                m.edit_config(target = "running", config = conf, default_operation = "merge")
                return "Loopback%s configured." % loopback_id
            except (RPCError) as e:
                return "%s: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask" % (e.__class__)

        return configure_loopback_call_edit_config()

    @_check_arguements_decorator
    def delete_loopback(self, loopback_id):
        '''
        Deletes a given loopback interface
        :param self: self
        :param loopback_id: id number for the loopback being deleted
        :return: delete_loopback_call_edit_config(), which calls m.edit_config(target = "running", config = conf, default_operation = "merge")
        '''

        conf = delete_loopback_xml_renderer(loopback_id)

        #function calling edit config, to be run if above tests pass. Decorator opens ssh connection
        @self._connect_ssh_decorator(conf)
        def delete_loopback_call_edit_config(m):
            '''
            Calls edit config with parameters to delete a loopback interface
            :param m: ncclient.manager.connect_ssh as m, passed through by decorator
            :return: m.edit_config(target = "running", config = conf, default_operation = "merge")
            '''
            
            try:
                m.edit_config(target = "running", config = conf, default_operation = "merge")
                return "Loopback%s deleted." % loopback_id
            except (RPCError) as e:
                return "%s: Interface deletion error - loopback id may not correspond with existing loopback interface" % e.__class__

        return delete_loopback_call_edit_config()

    @_check_arguements_decorator
    def list_interfaces(self):
        '''
        Calls get config
        :param self: self
        :return:list_interfaces_call_get_config(), which calls parseString(str(interface_xml)).toprettyxml()
        '''

        conf = list_interfaces_xml_renderer

        #function calling edit config, to be run if above tests pass. Decorator opens ssh connection
        @self._connect_ssh_decorator(conf)
        def list_interfaces_call_get_config(m):
            '''
            Calls get config
            :param m: ncclient.manager.connect_ssh as m, passed through by decorator
            :return: xml of all listed interfaces
            '''

            interface_xml = m.get(filter = ("subtree", conf))
            return parseString(str(interface_xml)).toprettyxml()

        return list_interfaces_call_get_config()