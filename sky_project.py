from ncclient import manager

class Router():
    def configure_loopback(self, host, port, username, password):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :return: None
        '''

        with manager.connect_ssh(
            host = host,
            port = port,
            username = username,
            password = password,
            hostkey_verify=False,
            device_params={"name":"csr"}) as m:
            pass