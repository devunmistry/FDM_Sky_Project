def configure_loopback_xml_renderer(loopback_id, loopback_ip, loopback_subnet_mask):
    '''
    Generates xml string for configuring loopback interface
    :param loopback_id: id number for the loopback being configured
    :param loopback_ip: ip address for the loopback being configured
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
""" % (loopback_id, loopback_ip, loopback_subnet_mask)

    return out