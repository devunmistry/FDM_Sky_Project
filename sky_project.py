from ipaddress import ip_address
from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SSHError
from ncclient.operations.rpc import RPCError
from socket import gaierror

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

        try: #check router socket ip address is of valid format
            ip_address(host)
        except(ValueError) as e:
            print("%s: Invalid ip address for router socket" % (e.__class__))
            return

        if type(port) is not int or port < 1 or port > 65535: #check router socket port is of valid format
            print("Invalid port for router socket")
            return

        if type(loopback_id) is not int or loopback_id < 0 or loopback_id > 2147483647: #check loopback id is of valid format
            print("Invalid id for loopback interface")
            return
        
        try: #check loopback ip address is of valid format
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

        except (gaierror, SSHError) as e:
            print ("%s: Could not open router socket %s:%s - could be incorrect ip address and/or port number" % (e.__class__, host, port))
        except (AuthenticationError) as e:
            print("%s: Incorrect router SSH username and/or password" % (e.__class__))
        except (RPCError) as e:
            print("%s: loopback interface configuration error - various possible causes, including unavailable ip address or invalid subnet mask" % (e.__class__))