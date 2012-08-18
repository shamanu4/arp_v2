# -*- encoding: utf-8 -*-

import sys

SERVER_IP = '127.0.0.1'
RELAY_VLAN = 66
RELAY_IP = "176.98.68.1"
HWADDR = "00:11:25:2c:18:e6"
DHCP_SUBNET_ADDR = "176.98.65.0"
DHCP_SUBNET_MASK = 24
DHCP_SUBNET_MASK_LITTLE = 29
DHCP_SUBNET_GATEWAY = "176.98.65.10"

print sys.path
import settings


from mock import MagicMock
from django.utils import unittest
from factories import DHCPServerFactory, DHCPDiscoverPacketFactory
from models import Subnet, Pool, Map, StaticMap, Lease
from lib.netutils import Network

class DHCPServerTestCase(unittest.TestCase):
    def setUp(self):
        self.server = DHCPServerFactory()
        self.dhcp_dp = DHCPDiscoverPacketFactory(hwaddr=HWADDR,relay_ip=RELAY_IP)
        self.dhcp_dp_wrong_relay = DHCPDiscoverPacketFactory(hwaddr=HWADDR,relay_ip="176.98.33.76")
        self.dhcp_dp_wrong_mac = DHCPDiscoverPacketFactory(hwaddr="00:aa:bb:cc:dd:ee",relay_ip=RELAY_IP)
        self.dhcp_dp_vlan = DHCPDiscoverPacketFactory(hwaddr=HWADDR,relay_ip=RELAY_IP,relay_vlan=RELAY_VLAN)
        self.dhcp_dp_wrong_vlan = DHCPDiscoverPacketFactory(hwaddr=HWADDR,relay_ip=RELAY_IP,relay_vlan=99)

    def test_evaluate_relay(self):
        """Check if packet has correctly relay set and relay properly readed from config"""
        self.assertEqual(self.server._evaluateRelay(self.dhcp_dp), True)
        self.assertEqual(self.server._evaluateRelay(self.dhcp_dp_wrong_relay), False)

    def test_handle_dhcp_discover(self):
        """Check if dhcp server """
        self.server._sendDHCPPacket = MagicMock()
        self.server._handleDHCPDiscover(self.dhcp_dp, SERVER_IP,False)
        self.assertEqual(self.server._sendDHCPPacket.called,True)

    def test_handle_dhcp_discover_wrong_mac(self):
        """Check if dhcp server """
        self.server._sendDHCPPacket = MagicMock()
        self.server._handleDHCPDiscover(self.dhcp_dp_wrong_mac, SERVER_IP,False)
        self.assertEqual(self.server._sendDHCPPacket.called,False)

    def test_handle_dhcp_discover_vlan(self):
        """Check if dhcp server """
        self.server._sendDHCPPacket = MagicMock()
        self.server._handleDHCPDiscover(self.dhcp_dp_vlan, SERVER_IP,False)
        self.assertEqual(self.server._sendDHCPPacket.called,True)

    def test_handle_dhcp_discover_wrong_vlan(self):
        """Check if dhcp server """
        self.server._sendDHCPPacket = MagicMock()
        self.server._handleDHCPDiscover(self.dhcp_dp_wrong_vlan, SERVER_IP,False)
        self.assertEqual(self.server._sendDHCPPacket.called,False)



class SubnetTestCase(unittest.TestCase):

    def setUp(self):
        self.sub = Subnet()
        self.sub.pool_destroy = MagicMock()
        self.sub.pool_create = MagicMock()
        self.sub.netaddr=DHCP_SUBNET_ADDR
        self.sub.mask=DHCP_SUBNET_MASK
        self.sub.save()

    def test_subnet_create(self):
        self.assertEqual(self.sub.__unicode__(),"%s/%s" % (DHCP_SUBNET_ADDR,DHCP_SUBNET_MASK))

    def test_subnet_has_gateway(self):
        self.assertEqual(self.sub.gateway,Network(self.sub.__unicode__()).host_first().dq)

    def test_subnet_has_correct_broadcast(self):
        self.assertEqual(self.sub.broadcast,Network(self.sub.__unicode__()).broadcast().dq)

    def test_subnet_too_small(self):
        self.sub.mask=31
        with self.assertRaisesRegexp(ValueError,"Network mask must be at least /30"):
            self.sub.save()

    def test_subnet_set_gateway(self):
        self.sub.gateway = DHCP_SUBNET_GATEWAY
        self.sub.save()
        self.assertEqual(self.sub.gateway,DHCP_SUBNET_GATEWAY)

    def test_subnet_set_wrong_gateway_a(self):
        self.sub.gateway = "10.10.10.10"
        with self.assertRaisesRegexp(ValueError,"Gateway address must belong to subnet"):
            self.sub.save()

    def test_subnet_set_wrong_gateway_b(self):
        self.sub.gateway = self.sub.netaddr
        with self.assertRaisesRegexp(ValueError,"Gateway must not be equal to network address"):
            self.sub.save()

    def test_subnet_set_wrong_gateway_c(self):
        self.sub.gateway = self.sub.broadcast
        with self.assertRaisesRegexp(ValueError,"Gateway must not be equal to broadcast address"):
            self.sub.save()

    def test_subnet_set_broadcast_ignore(self):
        self.sub.broadcast = "10.10.10.10"
        self.sub.save()
        self.test_subnet_has_correct_broadcast()

    def test_subnet_set_ntp(self):
        self.sub.ntp="ua.pool.ntp.org"
        self.sub.save()
        self.sub.ntp="212.111.205.110"
        self.sub.save()
        self.sub.ntp="212.111.205.110, 212.111.205.111"
        self.sub.save()
        self.sub.ntp="ua.pool.ntp.org, de.pool.ntp.org"
        self.sub.save()
        self.sub.ntp="ua.pool.ntp.org de.pool.ntp.org"
        self.sub.save()
        self.sub.ntp="212.111.205.110; 212.111.205.111;"
        self.sub.save()
        self.sub.ntp="ua.pool.ntp.org, 212.111.205.110"
        with self.assertRaisesRegexp(ValueError,"%s contains both IPv4 and DNS-based entries" % self.sub.ntp):
            self.sub.save()
        self.sub.ntp="212.111.205.110, 212.111.205.111, 212.111.205.112, 212.111.205.113"
        with self.assertRaises(ValueError):
            self.sub.save()

    def test_subnet_set_dns(self):
        """
        Logic of dns field is the same as ntp. So we don't need full testing.
        """
        self.sub.dns="dns.com.ua"
        self.sub.save()



class PoolTestCase(unittest.TestCase):

    def setUp(self):
        self.sub = Subnet(netaddr=DHCP_SUBNET_ADDR,mask=DHCP_SUBNET_MASK_LITTLE)
        self.sub.save()

    def tearDown(self):
        self.sub.delete()

    def test_create_pool_on_subnet_save(self):
        pool_objects = Pool.objects.filter(subnet=self.sub)
        self.assertEqual(pool_objects.count(),self.sub.network.size()-2)

    def test_destroy_pool(self):
        pool_objects = Pool.objects.filter(subnet=self.sub)
        self.assertEqual(pool_objects.count(),self.sub.network.size()-2)
        self.sub.pool_destroy()
        self.assertEqual(pool_objects.count(),0)

    def test_pool_gateway_used(self):
        pool_gateway = Pool.objects.get(subnet=self.sub,used=True)
        self.assertEqual(pool_gateway.ip,self.sub.gateway)

    def test_pool_use_static(self):
        ip=self.sub.network.host(2).dq
        map = Map(subnet=self.sub)
        map.save()
        static = StaticMap(map=map,ip=ip)
        static.save()
        pool_entry = Pool.objects.get(ip=ip)
        self.assertEqual(pool_entry.used,True)
        self.assertEqual(pool_entry.map,map)
        static.delete()
        pool_entry = Pool.objects.get(ip=ip)
        self.assertEqual(pool_entry.used,False)
        self.assertEqual(pool_entry.map,None)

    def test_pool_use_lease(self):
        ip=self.sub.network.host(2).dq
        map = Map(subnet=self.sub)
        map.save()
        lease = Lease(map=map,ip=ip)
        lease.save()
        pool_entry = Pool.objects.get(ip=ip)
        self.assertEqual(pool_entry.used,True)
        self.assertEqual(pool_entry.map,map)
        lease.delete()
        pool_entry = Pool.objects.get(ip=ip)
        self.assertEqual(pool_entry.used,False)
        self.assertEqual(pool_entry.map,None)






