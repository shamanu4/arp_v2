# -*- encoding: utf-8 -*-

import factory
from mock import MagicMock
from lib.libpydhcpserver.dhcp_packet import DHCPPacket
from lib.libpydhcpserver.dhcp_constants import DHCP_FIELDS
from dhcpd.dhcp import DHCPService
from dhcpd.dhcp import _DHCPServer
from dhcpd.models import Subnet

DHCPService._bindToAddress = MagicMock()

class DHCPServerFactory(_DHCPServer):

    def __init__(self):
        import threading
        import sql
        self._stats_lock = threading.Lock()
        self._dhcp_assignments = {}
        self._ignored_addresses = []
        self._sql_broker = sql.SQL_BROKER()



class DHCPPacketFactory(DHCPPacket):

    def __init__(self,*args,**kwargs):
        import random
        super(DHCPPacketFactory,self).__init__()            # initialize pachet data with magic cookie
        self.setOption("htype",random.choice(([1],[6])))    # set ethernet type to 10mbit (1) or IEEE 802 (6)
        self.setOption("hlen",[6])                          # Hardware Address Length: Specifies how long hardware addresses are in this message. For Ethernet or other networks using IEEE 802 MAC addresses, the value is 6.
        self.set_xid()
        if "hwaddr" in kwargs:
            self.set_hwaddr(kwargs["hwaddr"])
        if "relay_ip" in kwargs:
            self.set_hops(1)
            self.set_relay_ip(kwargs["relay_ip"])
            if "relay_vlan" in kwargs:
                self.set_relay_vlan(kwargs["relay_vlan"])
        #print self._packet_data

    def set_relay_vlan(self,vlan):
        from lib.libpydhcpserver.type_rfc import intToList
        data = [1,4,0,0]
        data = data + intToList(vlan)
        self.setOption("relay_agent",data)

    def set_relay_ip(self,ip):
        from lib.libpydhcpserver.type_rfc import ipToList
        data = ipToList(ip)
        self.setOption("giaddr",data)

    def set_xid(self,xid=0):
        import random
        from lib.libpydhcpserver.type_rfc import longToList
        if not xid:
            xid = int(random.getrandbits(32))
        data = longToList(xid)
        self.setOption("xid",data)

    def set_hwaddr(self,hwaddr):
        from lib.libpydhcpserver.type_hwmac import hwmac
        data = hwmac(hwaddr).list()
        self.setOption("chaddr",data)

    def set_hops(self,hops):
        self.setOption("hops",[hops])



class DHCPDiscoverPacketFactory(DHCPPacketFactory):

    def __init__(self,*args,**kwargs):
        super(DHCPDiscoverPacketFactory,self).__init__(*args,**kwargs)
        """
        self._packet_data = [1, 6, 6, 1, 171, 156, 47, 170, 0, 0, 128, 0, 0, 0, 0, 0, 176, 98, 80, 2, 0, 0, 0, 0, 176,
                             98, 95, 1, 0, 17, 37, 44, 24, 230, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 99, 130, 83, 99]
        """
        """
        self._options_data = {
                              #'server_identifier': [192, 168, 33, 152],
                              #'broadcast_address': [176, 98, 95, 255],
                              #'router': [176, 98, 68, 1],
                              #'ntp_servers': [192, 168, 33, 125],
                              #'auto_config': [1],
                              #'hostname': [108, 97, 112, 116, 111, 112, 50],
                              #'domain_name_servers': [192, 168, 33, 125],
                              #'domain_name': [105, 116, 45, 116, 105, 109],
                              #'subnet_mask': [255, 255, 224, 0],
                              #'relay_agent': [1, 6, 0, 4, 0, 66, 8, 23, 2, 8, 0, 6, 0, 5, 116, 222, 244, 0],
                              #'requested_ip_address': [176, 98, 80, 2],
                              #'dhcp_message_type': [2],
                              #'ip_address_lease_time': [0, 0, 46, 224]
                             }
        """
        #self._requested_options = (1, 3, 6, 33, 43, 44, 46, 15, 59, 51, 53, 54, 249, 58, 47, 31)

        self.setOption("op",[1])                # set dhcp packet type to dhcp-request




#class SubnetFactory(factory.Factory):
#
#    FACTORY_FOR = Subnet
#
#    netaddr = factory.LazyAttributeSequence(lambda a, n: '10.{n}.0.0'.format(n))
#    mask = 24
#    domain = factory.LazyAttributeSequence(lambda a, n: 'domain{0}.it-tim.net'.format(n))
