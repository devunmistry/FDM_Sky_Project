from ncclient import manager

class Router():
    def configure_loopback(self):
        '''
        Configures a given loopback interface using given parameters
        :param self: self
        :return: None
        '''

        with manager.connect_ssh(
            host = "192.168.0.101",
            port = "830",
            username = "cisco",
            password = "cisco",
            hostkey_verify=False,
            device_params={"name":"csr"}) as m:
            print("connected")