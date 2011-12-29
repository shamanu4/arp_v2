# -*- encoding: utf-8 -*-
"""
staticDHCPd module: src.conf

Purpose
=======
 Provides a buffer to seed options with default values to make upgrading easier
 for end users who do not need to manage any newly added features.
 
Legal
=====
 This file is part of staticDHCPd.
 staticDHCPd is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.
 
 (C) Neil Tallim, 2011 <red.hamsterx@gmail.com>
"""

"""
 headers for aptana built-in  syntax checker
"""

ALLOWED_DHCP_RELAYS=None
ALLOW_DHCP_RELAYS=None
ALLOW_LOCAL_DHCP=None
AUTHORITATIVE=None
DATABASE_ENGINE=None
DEBUG=None
DHCP_CLIENT_PORT=None
DHCP_SERVER_IP=None
DHCP_SERVER_PORT=None
EMAIL_DESTINATION=None
EMAIL_ENABLED=None
EMAIL_PASSWORD=None
EMAIL_SERVER=None
EMAIL_SOURCE=None
EMAIL_TIMEOUT=None
EMAIL_USER=None
ENABLE_SUSPEND=None
GID=None
LOG_CAPACITY=None
LOG_FILE=None
LOG_FILE_TIMESTAMP=None
MISBEHAVING_CLIENT_TIMEOUT=None
MYSQL_DATABASE=None
MYSQL_HOST=None
MYSQL_MAXIMUM_CONNECTIONS=None
MYSQL_PASSWORD=None
MYSQL_PORT=None
MYSQL_USERNAME=None
NAK_RENEWALS=None
ORACLE_DATABASE=None
ORACLE_MAXIMUM_CONNECTIONS=None
ORACLE_PASSWORD=None
ORACLE_USERNAME=None
PID_FILE=None
POLLING_INTERVAL=None
POLL_INTERVALS_TO_TRACK=None
POSTGRESQL_DATABASE=None
POSTGRESQL_HOST=None
POSTGRESQL_MAXIMUM_CONNECTIONS=None
POSTGRESQL_PASSWORD=None
POSTGRESQL_PORT=None
POSTGRESQL_SSLMODE=None
POSTGRESQL_USERNAME=None
PXE_PORT=None
SQLITE_FILE=None
SUSPEND_THRESHOLD=None
SYSTEM_NAME=None
UID=None
UNAUTHORIZED_CLIENT_TIMEOUT=None
USE_CACHE=None
USE_POOL=None
VERSION=None
WEB_ENABLED=None
WEB_IP=None
WEB_PORT=None
WEB_RELOAD_KEY=None
init=None
intToList=None
intsToList=None
ipToList=None
ipsToList=None
loadDHCPPacket=None
longToList=None
longsToList=None
rfc1035_plus=None
rfc2610_78=None
rfc2610_79=None
rfc3046_decode=None
rfc3361_120=None
rfc3397_119=None
rfc3925_124=None
rfc3925_125=None
rfc4174_83=None
rfc4280_88=None
rfc5223_137=None
rfc5678_139=None
rfc5678_140=None
strToList=None
strToPaddedList=None

"""
  end of headers
"""


import conf
#Options passed through from conf.py
#For explanations, please consult that file.
##############################################################################
_defaults = {}

#General settings
#######################################
_defaults.update({
 'DEBUG': False,
 
 'POLLING_INTERVAL': 30,
 'LOG_CAPACITY': 1000,
 'POLL_INTERVALS_TO_TRACK': 20,
})

#Server settings
#######################################
_defaults.update({
 'PXE_PORT': None,
})

#Server behaviour settings
#######################################
_defaults.update({
 'ALLOW_LOCAL_DHCP': True,
 'ALLOW_DHCP_RELAYS': True,
 'ALLOWED_DHCP_RELAYS': ("192.168.66.1",),

 'AUTHORITATIVE': True,

 'NAK_RENEWALS': False,

 'UNAUTHORIZED_CLIENT_TIMEOUT': 60,
 'MISBEHAVING_CLIENT_TIMEOUT': 150,
 'ENABLE_SUSPEND': True,
 'SUSPEND_THRESHOLD': 10,

 'WEB_RELOAD_KEY': '5f4dcc3b5aa765d61d8327deb882cf99',
})

#Database settings
#######################################
_defaults.update({
 'USE_CACHE': False,

 'USE_POOL': True,

 'MYSQL_DATABASE': 'dhcp',
 'MYSQL_USERNAME': 'dhcp_user',
 'MYSQL_PASSWORD': 'dhcp_pass',
 'MYSQL_HOST': None,
 'MYSQL_PORT': 3306,
 'MYSQL_MAXIMUM_CONNECTIONS': 4,

 'POSTGRESQL_DATABASE': 'dhcp',
 'POSTGRESQL_USERNAME': 'dhcp_user',
 'POSTGRESQL_PASSWORD': 'dhcp_pass',
 'POSTGRESQL_HOST': None,
 'POSTGRESQL_PORT': 5432,
 'POSTGRESQL_SSLMODE': 'disabled',
 'POSTGRESQL_MAXIMUM_CONNECTIONS': 4,

 'ORACLE_DATABASE': 'dhcp',
 'ORACLE_USERNAME': 'dhcp_user',
 'ORACLE_PASSWORD': 'dhcp_pass',
 'ORACLE_MAXIMUM_CONNECTIONS': 4,

 'SQLITE_FILE': '/etc/staticDHCPd/dhcp.sqlite3',
})

#E-mail settings
#######################################
_defaults.update({
 'EMAIL_ENABLED': False,
 'EMAIL_SERVER': 'mail.yourdomain.com',
 'EMAIL_SOURCE': 'you@yourdomain.com',
 'EMAIL_DESTINATION': 'problems@yourdomain.com',
 'EMAIL_USER': 'you',
 'EMAIL_PASSWORD': 'password',
 'EMAIL_TIMEOUT': 600,
})


#Construct a unified namespace
#######################################
for key in [k for k in dir(conf) if k.isupper()]: #Copy everything that looks like a constant.
    globals()[key] = getattr(conf, key)

for (key, value) in _defaults.iteritems():
    if not key in globals():
        globals()[key] = value
del _defaults

init = conf.init
loadDHCPPacket = conf.loadDHCPPacket

#Inject namespace elements into conf.
##############################################################################
import libpydhcpserver.type_rfc as type_rfc
conf.rfc3046_decode = type_rfc.rfc3046_decode
conf.rfc1035_plus = type_rfc.rfc1035_plus

conf.ipToList = type_rfc.ipToList
conf.ipsToList = type_rfc.ipsToList
conf.intToList = type_rfc.intToList
conf.intsToList = type_rfc.intsToList
conf.longToList = type_rfc.longToList
conf.longsToList = type_rfc.longsToList
conf.strToList = type_rfc.strToList
conf.strToPaddedList = type_rfc.strToPaddedList

conf.rfc2610_78 = type_rfc.rfc2610_78
conf.rfc2610_79 = type_rfc.rfc2610_79
conf.rfc3361_120 = type_rfc.rfc3361_120
conf.rfc3397_119 = type_rfc.rfc3397_119
conf.rfc3925_124 = type_rfc.rfc3925_124
conf.rfc3925_125 = type_rfc.rfc3925_125
conf.rfc4174_83 = type_rfc.rfc4174_83
conf.rfc4280_88 = type_rfc.rfc4280_88
conf.rfc5223_137 = type_rfc.rfc5223_137
conf.rfc5678_139 = type_rfc.rfc5678_139
conf.rfc5678_140 = type_rfc.rfc5678_140
del type_rfc


