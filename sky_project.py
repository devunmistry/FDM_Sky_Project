from ipaddress import ip_address
from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SSHError
from ncclient.operations.rpc import RPCError 
from functools import wraps

from xml_functions.xml_function_configure_loopback import configure_loopback_xml_renderer

class Router():

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def _connect_ssh_decorator(func):
        '''
        Decorator. Opens ssh connection with router. Wrapper function is connect_ssh_decorator_wrapper
        :param func: function to be wrapped within decorator
        :return: connect_ssh_decorator_wrapper
        '''

        @wraps(func)
        def connect_ssh_decorator_wrapper(self, *args):
            '''
            Decorator wrapper. Calls ncclient.manager.connect_ssh to open ssh connection with router
            :param self: self
            :param *args: arguements to be passed to wrapped function
            :return: none 
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
                        return func(self, *args, m)
            except (SSHError) as e:
                print ("%s: Could not open router socket %s:%s - could be incorrect ip address and/or port number" % (e.__class__, self.host, self.port))
            except (AuthenticationError) as e:
                print("%s: Incorrect router SSH username and/or password" % (e.__class__))

        return connect_ssh_decorator_wrapper
    
    @_connect_ssh_decorator
    def configure_loopback(self, loopback_id, loopback_ip, loopback_subnet_mask, m):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :param loopback_id: id number for the loopback being configured
        :param loopback_ip: ip address for the loopback being configured
        :param loopback_subnet_mask: subnet mask for the loopback being configured
        :param m: ***DO NOT DEFINE - GIVEN BY DECORATOR*** open connection, passed from _connect_ssh_decorator
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

        try:
            conf = configure_loopback_xml_renderer(loopback_id, loopback_ip, loopback_subnet_mask)
            m.edit_config(target = "running", config = conf, default_operation = "merge")
        except (RPCError) as e:
            print("%s: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask" % (e.__class__))

    @_connect_ssh_decorator
    def delete_loopback(self, m):
        '''
        Deletes a given loopback interface
        :param self: self
        :param m: ***DO NOT DEFINE - GIVEN BY DECORATOR*** open connection, passed from _connect_ssh_decorator
        :return: None
        '''

        conf = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback operation="delete">
                <name>1</name>
            </Loopback>
        </interface>
    </native>
</config>
"""
        m.edit_config(target = "running", config = conf, default_operation = "merge")