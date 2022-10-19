from pysnmp.hlapi import *


def oid_query(community, version, port,  ip_add, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=version),
        UdpTransportTarget((ip_add, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    data = ""
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        data = errorIndication

    elif errorStatus:
        data = ('%s at %s' % (errorStatus.prettyPrint(),
                              errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            data += ' = '.join([x.prettyPrint() for x in varBind])

    return data
