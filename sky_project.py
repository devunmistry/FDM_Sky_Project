from ipaddress import ip_address
from functools import wraps
from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SSHError
from ncclient.operations.rpc import RPCError 
from xml.dom.minidom import parseString

from xml_functions.xml_function_configure_loopback import configure_loopback_xml_renderer
from xml_functions.xml_function_delete_loopback import delete_loopback_xml_renderer
from xml_functions.xml_function_list_interfaces import list_interfaces_xml_renderer

class Router():

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dry_run = 0

    ####################
    ## Decorators     ##
    ####################
    
    def _test_host_port_decorator(func):
        '''
        Decorator. Tests the router host and port are of the correct format. Should be called before Class functions.
        :param func: function to be wrapped within decorator.
        :return: test_host_port_decorator_wrapper
        '''

        @wraps(func)
        def test_host_port_decorator_wrapper(self, *args):
            '''
            Decorator wrapper. Includes try/except for router host, and if statement for router port.
            :param self: self
            :param *args: arguements to be passed to wrapped function
            :return: func(*args)
            '''

            #check router socket ip address is of valid format
            try:
                ip_address(self.host)
            except(ValueError) as e:
                print("%s: Invalid ip address for router socket" % (e.__class__))
                return

            #check router socket port is of valid format
            if type(self.port) is not int or self.port < 1 or self.port > 65535:
                print("Invalid port for router socket")
                return
            
            return func(self, *args)
        
        return test_host_port_decorator_wrapper

    def _connect_ssh_decorator(self, func):
        '''
        Decorator. Opens ssh connection with router. Should be called within Class functions.
        :param self: self
        :param func: function to be wrapped within decorator
        :return: connect_ssh_decorator_wrapper
        '''

        def connect_ssh_decorator_wrapper(*args):
            '''
            Decorator wrapper. Calls ncclient.manager.connect_ssh to open ssh connection with router
            :param *args: arguements to be passed to wrapped function
            :return: func(*args, m)
                     m is ncclient.manager.connect_ssh
            '''

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
                print ("%s: Could not open router socket %s:%s - could be incorrect ip address and/or port number" % (e.__class__, self.host, self.port))
            except (AuthenticationError) as e:
                print("%s: Incorrect router SSH username and/or password" % (e.__class__))

        return connect_ssh_decorator_wrapper

    ####################
    ## Getters & setters ##
    ####################

    def change_dry_run(self):
        self.dry_run = abs(self.dry_run - 1)
        if self.dry_run == 0:
            print("dry_run = 0: Payload will be sent to router")
        if self.dry_run == 1:
            print("dry_run = 1: Payload will be returned to user")

    ####################
    ## Methods        ##
    ####################

    @_test_host_port_decorator
    def configure_loopback(self, loopback_id, loopback_ip, loopback_subnet_mask):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :param loopback_id: id number for the loopback being configured
        :param loopback_ip: ip address for the loopback being configured
        :param loopback_subnet_mask: subnet mask for the loopback being configured
        :return: None
        '''

        #check loopback id is of valid format
        if type(loopback_id) is not int or loopback_id < 0 or loopback_id > 2147483647:
            print("Invalid id for loopback interface")
            return
        
        #check loopback ip address is of valid format
        try:
            ip_address(loopback_ip)
        except(ValueError) as e:
            print("%s: Invalid ip address for loopback interface" % (e.__class__))
            return

        #check loopback subnet mask is of valid format
        try:
            ip_address(loopback_subnet_mask)
        except(ValueError) as e:
            print("%s: Invalid subnet mask for loopback interface" % (e.__class__))
            return

        # define function calling edit config, to be run if above tests pass. Decorator opens ssh connection
        @self._connect_ssh_decorator
        def _configure_loopback_call_edit_config(m):
            '''
            Calls edit config with parameters to create/edit a loopback interface
            :param m: ncclient.manager.connect_ssh as m, passed through by decorator
            :return: None
            '''

            m.edit_config(target = "running", config = conf, default_operation = "merge")

        try:
            conf = configure_loopback_xml_renderer(loopback_id, loopback_ip, loopback_subnet_mask)
            if self.dry_run == 1:
                return conf
            _configure_loopback_call_edit_config()
        except (RPCError) as e:
            print("%s: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask" % (e.__class__))

    @_test_host_port_decorator
    def delete_loopback(self, loopback_id):
        '''
        Deletes a given loopback interface
        :param self: self
        :param loopback_id: id number for the loopback being deleted
        :return: None
        '''
        
        #check loopback ip address is of valid format
        if type(loopback_id) is not int or loopback_id < 0 or loopback_id > 2147483647:
            print("Invalid id for loopback interface")
            return
        
        #function calling edit config, to be run if above tests pass. Decorator opens ssh connection
        @self._connect_ssh_decorator
        def _delete_loopback_call_edit_config(m):
            '''
            Calls edit config with parameters to delete a loopback interface
            :param m: ncclient.manager.connect_ssh as m, passed through by decorator
            :return: None
            '''

            m.edit_config(target = "running", config = conf, default_operation = "merge")

        try:
            conf = delete_loopback_xml_renderer(loopback_id)
            _delete_loopback_call_edit_config()
        except (RPCError) as e:
            print("%s: Interface deletion error - loopback id may not correspond with existing loopback interface" % e.__class__)
    
    @_test_host_port_decorator
    def list_interfaces(self):
        '''
        Calls get config
        :param self: self
        :return:
        '''
        
        @self._connect_ssh_decorator
        def _list_interfaces_call_get_config(m):
            '''
            Calls get config
            :param m: ncclient.manager.connect_ssh as m, passed through by decorator
            :return: xml of all listed interfaces
            '''

            interface_xml = m.get(filter = ("subtree", list_interfaces_xml_renderer))
            print(parseString(str(interface_xml)).toprettyxml())
        
        _list_interfaces_call_get_config()