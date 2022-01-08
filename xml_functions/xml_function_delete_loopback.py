def delete_loopback_xml_renderer(loopback_id):
    '''
    Generates xml string for deleting loopback interface
    :param loopback_id: id number for the loopback being configured
    :return: xml string
    '''

    out = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback operation="delete">
                <name>%s</name>
            </Loopback>
        </interface>
    </native>
</config>
""" % (loopback_id)

    return str(out)