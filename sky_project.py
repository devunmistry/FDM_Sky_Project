from ipaddress import ip_address
from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SSHError
from socket import gaierror

from xml_functions.xml_function_configure_loopback import configure_loopback_xml_renderer

class Router():
    
    def configure_loopback(self, host, port, username, password, loopback_ID, loopback_IP, loopback_subnet_mask):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :param host: ip address for router
        :param port: port number for router ssh connection - normally 830, though have not set as default value
        :param username: username for router ssh login - privilege should have been set to 15 to allow necessary ssh access 
        :param password: password for router ssh login
        :param loopback_ID: id number for the loopback being configured
        :param loopback_IP: ip address for the loopback being configured
        :param loopback_subnet_mask: subnet mask for the loopback being configured
        :return: None
        '''

        try: #check router socket ip address is of valid format
            ip_address(host)
        except(ValueError) as e:
            print("%s: Invalid IP address for router socket" % (e.__class__))
            return

        if type(port) is not int or port < 1 or port > 65535: #check router socket port is of valid format
            print("Invalid port for router socket")
            return

        try:
            with manager.connect_ssh(
                host = host,
                port = port,
                username = username,
                password = password,
                hostkey_verify=False,
                device_params={"name":"csr"}) as m:
                    conf = configure_loopback_xml_renderer(loopback_ID, loopback_IP, loopback_subnet_mask)
                    m.edit_config(target = "running", config = conf, default_operation="merge")

        except (gaierror, SSHError) as e:
            print ("%s: Could not open router socket %s:%s - could be incorrect IP address and/or port number" % (e.__class__, host, port))
        except (AuthenticationError) as e:
            print("%s: Incorrect router SSH username and/or password" % (e.__class__))