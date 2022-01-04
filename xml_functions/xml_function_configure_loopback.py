def configure_loopback_xml_renderer(loopback_ID, loopback_IP, loopback_subnet_mask):
    '''
    Generates xml string for configuring loopback interface
    :param loopback_ID: id number for the loopback being configured
    :param loopback_IP: ip address for the loopback being configured
    :param loopback_subnet_mask: subnet mask for the loopback being configured
    :return: xml string
    '''

    out = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>%s</name>
                <ip>
                    <address>
                        <primary>
                            <address>%s</address>
                            <mask>%s</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
""" % (loopback_ID, loopback_IP, loopback_subnet_mask)
    return out