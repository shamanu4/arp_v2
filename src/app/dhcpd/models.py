# -*- encoding: utf-8 -*-

from django.db import models
from datetime import datetime, timedelta



class Subnet(models.Model):

    netaddr = models.IPAddressField()
    mask = models.IntegerField(default=24)
    gateway = models.IPAddressField(blank=True)
    broadcast = models.IPAddressField(blank=True)
    ntp = models.CharField(max_length=40,blank=True,null=True)
    dns = models.CharField(max_length=40,blank=True,null=True)
    domain = models.CharField(blank=True,max_length=20,default="my.domain")
    lease_time = models.IntegerField(default=43200)
    comment = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return "%s/%s" % (self.netaddr,self.mask)

    def save(self,*args,**kw):
        # TODO: move data validation to form and call form validation from here
        from lib.netutils import Network
        from lib.libpydhcpserver.type_rfc import rfc3361_120
        net = Network(self.__unicode__())
        if net.size() < 4:
            raise ValueError, "Network mask must be at least /30"
        if not self.gateway:
            self.gateway = net.host_first().dq
        else:
            if not net.has_key(self.gateway):
                raise ValueError, "Gateway address must belong to subnet"
            if self.gateway == net.broadcast().dq:
                raise ValueError, "Gateway must not be equal to broadcast address"
            if self.gateway == net.network().dq:
                raise ValueError, "Gateway must not be equal to network address"
        self.broadcast = net.broadcast().dq
        if self.ntp:
            rfc3361_120(self.ntp[0:40])
        if self.dns:
            rfc3361_120(self.dns[0:40])
        super(Subnet,self).save()
        self.pool_destroy()
        self.pool_create()

    def delete(self,*args,**kw):
        self.pool_destroy()
        super(Subnet,self).delete(*args,**kw)

    @property
    def network(self):
        from lib.netutils import Network
        return Network(self.__unicode__())

    def pool_destroy(self):
        self.pool.all().delete()

    def pool_create(self):
        for host in self.network:
            if host.dq == self.netaddr or host.dq == self.broadcast:
                continue
            pool_entry = Pool(subnet=self,ip=host.dq)
            if host.dq == self.gateway:
                pool_entry.used = True
                pool_entry.save()
                continue
            try:
                static_entry = StaticMap.objects.get(ip=host.dq)
            except StaticMap.DoesNotExist:
                # IP not used in static maps. Continue looking in Dynamic leases
                try:
                    lease = Lease.objects.get(ip=host.dq)
                except Lease.DoesNotExist:
                    # IP not used in dynamic leases so left it marked as unused
                    pass
                else:
                    pool_entry.used=True
                    pool_entry.map=lease.map
            else:
                pool_entry.used=True
                pool_entry.map=static_entry.map
            try:
                pool_entry.save()
            except:
                print pool_entry




class Relay(models.Model):

    ip = models.IPAddressField(unique=True)
    name = models.CharField(max_length=20,blank=True,null=True)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        if self.enabled:
            return "%s" % (self.ip,)
        return "%s [x]" % (self.ip,)



class Map(models.Model):

    subnet = models.ForeignKey(Subnet)
    mac = models.CharField(max_length=17,blank=True,null=True)
    relay = models.ForeignKey(Relay,blank=True,null=True)
    vlan = models.IntegerField(blank=True,null=True)
    enabled = models.BooleanField(default=True)
    comment = models.TextField(blank=True,null=True)

    class Meta:
        unique_together = (
            ("mac", "relay", "vlan"),
        )

    def __unicode__(self):
        output = self.subnet.__unicode__()
        if self.mac:
            output += " mac[%s]" % self.mac
        if self.relay:
            output += " relay[%s]" % ( self.relay.name or self.relay.ip )
        if self.vlan:
            output += " vlan[%s]" % self.vlan
        if self.static and self.static.enabled:
            output += " static[%s]" % self.static.ip
        if not self.enabled:
            output += " [x]"
        return output



class StaticMap(models.Model):

    map = models.OneToOneField(Map,unique=True,related_name="static")
    ip = models.IPAddressField(unique=True)
    enabled = models.BooleanField(default=True)
    comment = models.TextField(blank=True,null=True)

    def __unicode__(self):
        if self.enabled:
            return self.map.__unicode__()
        else:
            return "%s static_disabled[%s]" % (self.map.__unicode__(),self.ip)

    def save(self,*args,**kw):
        try:
            pool_entry = Pool.objects.get(ip=self.ip)
        except Pool.DoesNotExist:
            raise ValueError, "Cannot save static map. IP address not in any dhcp pool."
        else:
            if pool_entry.used:
                raise ValueError, "Cannot save static map. IP address already used."
            if not pool_entry.subnet == self.map.subnet:
                raise ValueError, "Cannot save static map. IP address not in dhcp pool which belongs to address map."
            pool_entry.used=True
            pool_entry.map=self.map
            pool_entry.save()
        super(StaticMap,self).save(*args,**kw)

    def delete(self,*args,**kw):
        pool_entry = Pool.objects.get(ip=self.ip)
        pool_entry.used = False
        pool_entry.map = None
        pool_entry.save()
        super(StaticMap,self).delete(*args,**kw)



class Lease(models.Model):

    map = models.OneToOneField(Map,unique=True,related_name="lease")
    ip = models.IPAddressField(unique=True)
    mac = models.CharField(max_length=17)
    relay = models.ForeignKey(Relay,blank=True,null=True)
    vlan = models.IntegerField(blank=True,null=True)
    created = models.DateTimeField(default=datetime.now)
    expires = models.DateTimeField(default=lambda:datetime.now()+timedelta(hours=1))

    def __unicode__(self):
        return "LEASE: %s" % self.map.__unicode__()

    def save(self,*args,**kw):
        try:
            pool_entry = Pool.objects.get(ip=self.ip)
        except Pool.DoesNotExist:
            raise ValueError, "Cannot save lease. IP address not in any dhcp pool."
        else:
            if pool_entry.used:
                raise ValueError, "Cannot save lease. IP address already used."
            if not pool_entry.subnet == self.map.subnet:
                raise ValueError, "Cannot save lease. IP address not in dhcp pool which belongs to address map."
            pool_entry.used=True
            pool_entry.map=self.map
            pool_entry.save()
        super(Lease,self).save(*args,**kw)

    def delete(self,*args,**kw):
        pool_entry = Pool.objects.get(ip=self.ip)
        pool_entry.used = False
        pool_entry.map = None
        pool_entry.save()
        super(Lease,self).delete(*args,**kw)



class Pool(models.Model):
    """
    This model is a helper for dhcp server in IP lookup process.
    It contains all IP addresses from subnets and markers if this ip is used now or not.
    IP addresses with static mappings are used permanently.
    """
    subnet = models.ForeignKey(Subnet,related_name="pool")
    ip = models.IPAddressField(unique=True)
    used = models.BooleanField(default=False)
    map = models.ForeignKey(Map,blank=True,null=True,related_name="pool_entry")

    def __unicode__(self):
        if self.used:
            return "IP [%s] poll [%s]" % (self.ip,self)