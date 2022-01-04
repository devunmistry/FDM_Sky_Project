from ncclient import manager
from ncclient.transport.errors import SSHError

class Router():
    def configure_loopback(self, host, port, username, password):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
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
                pass
        except (SSHError):
            raise SSHError("Invalid IP address and/or port number")