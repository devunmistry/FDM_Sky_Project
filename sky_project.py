from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SSHError
from socket import gaierror

class Router():
    
    def configure_loopback(self, host, port, username, password):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :param host: ip address for router
        :param port: port number for router ssh connection - normally 830, though have not set as default value
        :param username: username for router ssh login - privilege should have been set to 15 to allow necessary ssh access 
        :param password: password for router ssh login
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
                    conf = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>1</name>
                <ip>
                    <address>
                        <primary>
                            <address>192.168.1.1</address>
                            <mask>255.255.255.0</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""
                    m.edit_config(target = "running", config = conf, default_operation="merge")

        except (gaierror):
            raise gaierror("Invalid IP address and/or port number")
        except (SSHError):
            raise SSHError("Could not open socket {}:{} - could be incorrect IP address and/or port number".format(host, port))
        except (AuthenticationError):
            raise AuthenticationError("Incorrect username and/or password")