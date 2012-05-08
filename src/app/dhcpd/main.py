# -*- encoding: utf-8 -*-
"""
staticDHCPd module: main

Purpose
=======
 Runs a staticDHCPd server.
 
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
 
 (C) Neil Tallim, 2009 <red.hamsterx@gmail.com>
"""
import os
import signal
import sys
import time

from dhcpd import conf_default as conf
from dhcpd import dhcp
from dhcpd import logging
from dhcpd import web

if not conf.DEBUG: #Suppress all unnecessary prints. 
    sys.stdout = sys.stderr = open('/dev/null', 'w')
else:
    sys.stdout = sys.stderr

#noinspection PyUnusedLocal,PyBroadException
def _quitHandler(signum, frame):
    """
    Cleanly shuts down this daemon upon receipt of a SIGTERM.
    
    @type signum: int
    @param signum: The kill-signal constant received. This will always be
        SIGTERM.
    @type frame: int
    @param frame: The stack-frame in which the kill-signal was received.
        This is not used.
    """
    #Remove PID.
    try:
        os.unlink(conf.PID_FILE)
    except:
        pass
        
    logging.logToDisk()
    
    exit(0)

#noinspection PyUnusedLocal
def _logHandler(signum, frame):
    """
    Flushes DHCP cache and writes log to disk upon receipt of a SIGHUP.
    
    @type signum: int
    @param signum: The kill-signal constant received. This will always be
        SIGHUP.
    @type frame: int
    @param frame: The stack-frame in which the kill-signal was received.
        This is not used.
    """
    dhcp.flushCache()
    if not logging.logToDisk():
        logging.writeLog("Unable to write logfile: %(log)s" % {'log': conf.LOG_FILE,})
    else:
        logging.writeLog("Wrote log to '%(log)s'" % {'log': conf.LOG_FILE,})
        
def run():
    #Ensure that pre-setup tasks are taken care of.
    conf.init()
    
    #Start Web server.
    if conf.WEB_ENABLED:
        web_thread = web.WebService()
        web_thread.start()
        
    #Start DHCP server.
    dhcp_thread = dhcp.DHCPService()
    dhcp_thread.start()
    
    #Record PID.
    #noinspection PyBroadException
    try:
        pidfile = open(conf.PID_FILE, 'w')
        pidfile.write(str(os.getpid()) + '\n')
        pidfile.close()
        os.chown(conf.PID_FILE, conf.UID, conf.GID)
    except:
        logging.writeLog("Unable to write pidfile: %(file)s" % {'file': conf.PID_FILE,})
        
    #Touch logfile.
    #noinspection PyBroadException
    try:
        open(conf.LOG_FILE, 'a').close()
        os.chown(conf.LOG_FILE, conf.UID, conf.GID)
    except:
        logging.writeLog("Unable to write pidfile: %(file)s" % {'file': conf.PID_FILE,})
        
    #Set signal-handlers.
    signal.signal(signal.SIGHUP, _logHandler)
    signal.signal(signal.SIGTERM, _quitHandler)
    
    #Set proper permissions for execution
    os.setregid(conf.GID, conf.GID)
    os.setreuid(conf.UID, conf.UID)
    
    #Serve until interrupted.
    tick = 0
    while True:
        time.sleep(1)
        
        tick += 1
        if tick >= conf.POLLING_INTERVAL: #Perform periodic cleanup.
            dhcp_thread.pollStats()
            logging.emailTimeoutCooldown()
            tick = 0
            
