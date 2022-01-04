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

        except (gaierror):
            raise gaierror("Invalid IP address and/or port number")
        except (SSHError):
            raise SSHError("Could not open socket {}:{} - could be incorrect IP address and/or port number".format(host, port))
        except (AuthenticationError):
            raise AuthenticationError("Incorrect username and/or password")