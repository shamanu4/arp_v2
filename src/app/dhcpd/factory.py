__author__ = 'shamanu4'

import factory

from lib.libpydhcpserver.dhcp_packet import DHCPPacket
from dhcpd.dhcp import DHCPService

class DHCPServerFactory(object):
    def __new__(cls):
        service = DHCPService()
        return service._dhcp_server

class DHCPPacketFactory(DHCPPacket):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.name = "Test Product"
        self.features = "Awesome feature set brah!"