#This file is interpreted by Python and it may be extended with any Python code
#you wish, allowing you to do things like query web services to get values.

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

#General settings
#######################################
#If True, all events will be printed to console.
DEBUG = True

#The name to use when referring to this system.
SYSTEM_NAME = 'staticDHCPd'
#The file to which logs should be dumped on receipt of TERM or HUP.
LOG_FILE = '/var/log/' + SYSTEM_NAME + '.log'
#True to write logfiles with the current timestamp; requires that staticDHCPd
#has write-access to the directory above, which may be a security risk.
LOG_FILE_TIMESTAMP = False
#The file to which PID information should be written.
PID_FILE = '/var/run/' + SYSTEM_NAME + '.pid'

#The frequency at which the DHCP server's stats will be polled, in seconds.
POLLING_INTERVAL = 30
#The number of events to keep in the server's log-buffer.
LOG_CAPACITY = 1000
#The amount of statistical information to track.
POLL_INTERVALS_TO_TRACK = 20

#Server settings
#######################################
#The UID that will run this daemon.
UID = 0
#The GID that will run this daemon.
GID = 0

#The IP of the interface on which DHCP responses should be sent.
#This value must be set to a real IP.
DHCP_SERVER_IP = '192.168.33.152'
#The port on which DHCP requests are to be received; 67 is the standard.
DHCP_SERVER_PORT = 67
#The port on which clients wait for DHCP responses; 68 is the standard.
DHCP_CLIENT_PORT = 68

#Set this to a port-number (4011 is standard) to enable PXE-processing.
PXE_PORT = None

#True to enable access to server statistics and logs.
WEB_ENABLED = True
#The IP of the interface on which the HTTP interface should be served.
#Use '0.0.0.0' to serve on all interfaces.
WEB_IP = '192.168.33.152'
#The port on which the HTTP interface should be served.
WEB_PORT = 30880

#Server behaviour settings
#######################################
#If False, local DHCP requests will be ignored.
ALLOW_LOCAL_DHCP = True
#If False, relayed DHCP requests will be ignored.
ALLOW_DHCP_RELAYS = True
#A list of all IPs allowed to relay requests; if empty, all are allowed.
ALLOWED_DHCP_RELAYS = ['192.168.66.1','176.98.68.1']

#If True, any unknown MACs will be NAKed instead of ignored. If you may have
#more than one DHCP server serving a single LAN, this is NOT something you
#should enable.
AUTHORITATIVE = False

#If True, REBIND and RENEW requests are NAKed when received, forcing clients to
#either wait out their lease or return to the DISCOVER phase.
NAK_RENEWALS = False

#The number of seconds for which to ignore unknown MACs.
UNAUTHORIZED_CLIENT_TIMEOUT = 60
#The number of seconds for which to ignore potentially malicious MACs.
MISBEHAVING_CLIENT_TIMEOUT = 150
#If True, MACs requesting too many addresses will be flagged as malicious.
ENABLE_SUSPEND = True
#The number of times a well-behaved MAC can search for or request an IP
#within the polling interval.
SUSPEND_THRESHOLD = 10

#MD5 of the password needed to reload config.
WEB_RELOAD_KEY = '5f4dcc3b5aa765d61d8327deb882cf99'

#Database settings
#######################################
#Allowed values: MySQL, PostgreSQL, Oracle, SQLite
DATABASE_ENGINE = 'MySQL'

#Controls whether DHCP data gleaned from database lookups should be cached until
#manually flushed; consumes more resources and adds a step before a MAC can be
#automatically NAKed or have its details updated, but dramatically improves
#performance under heavy loads.
USE_CACHE = False

#Controls whether SQL daemon connections are pooled. This only works if the
#eventlet library has been installed and you've chosen a pooling-friendly
#engine, which excludes SQLite.
USE_POOL = True

#MYSQL_* values used only with 'MySQL' engine.
#The name of your database.
MYSQL_DATABASE = 'dhcp'
#The name of a user with SELECT access.
MYSQL_USERNAME = 'dhcp_user'
#The password of the user.
MYSQL_PASSWORD = 'dhcp_pass'
#The host on which MySQL is running. None for 'localhost'.
MYSQL_HOST = None
#The port on which MySQL is running; ignored when HOST is None.
MYSQL_PORT = 3306
#The number of threads that may read the database at once.
MYSQL_MAXIMUM_CONNECTIONS = 4

#POSTGRESQL_* values used only with 'PostgreSQL' engine.
#The name of your database.
POSTGRESQL_DATABASE = 'dhcp'
#The name of a user with SELECT access.
POSTGRESQL_USERNAME = 'dhcp_user'
#The password of the user.
POSTGRESQL_PASSWORD = 'dhcp_pass'
#The host on which PostgreSQL is running. None for 'localhost'.
POSTGRESQL_HOST = None
#The port on which PostgreSQL is running; ignored when HOST is None.
POSTGRESQL_PORT = 5432
#The SSL mode to use; ignored when HOST is None.
#http://www.postgresql.org/docs/9.0/static/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS
POSTGRESQL_SSLMODE = 'disabled'
#The number of threads that may read the database at once.
POSTGRESQL_MAXIMUM_CONNECTIONS = 4

#ORACLE_* values used only with 'Oracle' engine.
#The name of your database (from tnsnames.ora).
ORACLE_DATABASE = 'dhcp'
#The name of a user with SELECT access.
ORACLE_USERNAME = 'dhcp_user'
#The password of the user.
ORACLE_PASSWORD = 'dhcp_pass'
#The number of threads that may read the database at once.
ORACLE_MAXIMUM_CONNECTIONS = 4

#SQLITE_* values used only with 'SQLite' engine.
#The file that contains your SQLite database.
SQLITE_FILE = '/etc/staticDHCPd/dhcp.sqlite3'

#E-mail settings
#######################################
#True to allow staticDHCPd to inform you of any problems it cannot handle by
#itself. (*Very* useful for development and fast troubleshooting)
EMAIL_ENABLED = False
#The server that receives your e-mail.
EMAIL_SERVER = 'mail.yourdomain.com'
#The user from which e-mail should claim to be sent.
EMAIL_SOURCE = 'you@yourdomain.com'
#The user to whom e-mail should be sent.
EMAIL_DESTINATION = 'problems@yourdomain.com'
#The user who should authenticate to the mail server.
#If None, SMTP authentication is not used.
EMAIL_USER = 'you'
#The password of the user who should authenticate to the mail server.
EMAIL_PASSWORD = 'password'
#The number of seconds to wait between sending e-mails.
EMAIL_TIMEOUT = 600

#DHCP-processing functions
#######################################
def init():
    #Perform any required imports or setup operations within this function.
    pass
    
def loadDHCPPacket(packet, mac, client_ip, relay_ip, subnet, serial, pxe, vendor):
    #This is a custom function, called before each packet is sent, that
    #allows you to tweak the options attached to a DHCP response.
    #
    #If, for any reason, you want to abort sending the packet, return False.
    #
    #If you need to add, test for, or delete an option, consult staticDHCPd's
    #rule-writing guide.
    #
    ##### PARAMETERS #####
    print "DEBUG:"
    print "packet: %s;;\n mac: %s;;\n client_ip: %s;;\n relay_ip: %s;;\n subnet: %s;;\n serial: %s;;\n pxe: %s;;\n vendor: %s;;\n" % (packet, mac, client_ip, relay_ip, subnet, serial, pxe, vendor)
    #mac is a human-readable MAC string, lower-case, separated by colons.
    #client_ip is a quadruple of octets: (192, 168, 1, 1)
    #relay_ip is either None or an address as a quadruple of octets,
    #    depending on whether this is a response to a relay request.
    #subnet and serial are values passed through from the database, as a
    #    string and int, respectively.
    #pxe is a boolean indicating whether the request was received on the PXE
    #    port (True) or not (False).
    #vendor is a four-tuple containing, in order, option 43
    #    (vendor_specific_information) as a string of bytes, option 60
    #    (vendor_class_identifier) as a string, and both option 124
    #    (vendor_class) and option 125 (vendor_specific) as digested data:
    #    [(enterprise_number:int, data:string)] and
    #    [(enterprise_number:int, [(subopt_code:byte, data:string)])],
    #    respectively. Any unset options are presented as None.
    return True
    
