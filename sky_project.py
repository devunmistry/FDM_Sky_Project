from ipaddress import ip_address
from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SSHError
from ncclient.operations.rpc import RPCError

from xml_functions.xml_function_configure_loopback import configure_loopback_xml_renderer

class Router():
    
    def configure_loopback(self, host, port, username, password, loopback_id, loopback_ip, loopback_subnet_mask):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :param host: ip address for router
        :param port: port number for router ssh connection - normally 830, though have not set as default value
        :param username: username for router ssh login - privilege should have been set to 15 to allow necessary ssh access 
        :param password: password for router ssh login
        :param loopback_id: id number for the loopback being configured
        :param loopback_ip: ip address for the loopback being configured
        :param loopback_subnet_mask: subnet mask for the loopback being configured
        :return: None
        '''

        #check router socket ip address is of valid format
        try:
            ip_address(host)
        except(ValueError) as e:
            print("%s: Invalid ip address for router socket" % (e.__class__))
            return

        #check router socket port is of valid format
        if type(port) is not int or port < 1 or port > 65535:
            print("Invalid port for router socket")
            return

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

        try:
            with manager.connect_ssh(
                host = host,
                port = port,
                username = username,
                password = password,
                hostkey_verify=False,
                device_params={"name":"csr"}) as m:
                    conf = configure_loopback_xml_renderer(loopback_id, loopback_ip, loopback_subnet_mask)
                    m.edit_config(target = "running", config = conf, default_operation="merge")

        except (SSHError) as e:
            print ("%s: Could not open router socket %s:%s - could be incorrect ip address and/or port number" % (e.__class__, host, port))
        except (AuthenticationError) as e:
            print("%s: Incorrect router SSH username and/or password" % (e.__class__))
        except (RPCError) as e:
            print("%s: Loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask" % (e.__class__))
    
    def delete_loopback(self):
        with manager.connect_ssh(
            host = "192.168.0.101",
            port = 830,
            username = "cisco",
            password = "cisco",
            hostkey_verify=False,
            device_params={"name":"csr"}) as m:
                pass