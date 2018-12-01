#!/usr/bin/python

import os, sys, signal
import argparse
from pprint import pprint, pformat
import threading
import time

from utils import Object
from carrier import *
from prompt import CmdThread

########################################################
# initialize

try:
  user = os.environ['USER']
except:
  user = None

home = os.environ['HOME']

libPath = home + '/dev/carrier/elastos-carrier-5.1.71e4c1-linux-x86_64-Debug/lib'
#libPath = home + '/Documents/Projects/elastos/Elastos.NET.Carrier.Native.SDK/build/win/outputs/lib'
# for building carrier w/modified code...
#libPath = home + '/dev/src/github.com/elastos/Elastos.NET.Carrier.Native.SDK/build/linux/src/carrier'
logPath = home + '/projects/pyelastos/elastos.log'
persistentPath = home + '/projects/pyelastos/elastos.data'
interval = 0
logLevel = 4

parser = argparse.ArgumentParser()
parser.add_argument('--lib', dest='libPath', default=libPath, help='directory path for libelacarrier.so, libelasession.so')
parser.add_argument('--log', dest='logPath', default=logPath, help='file path for log file ("" for none)')
parser.add_argument('--data', dest='dataPath', default=persistentPath, help='file path for persistent data ("" for none)')
parser.add_argument('--interval', dest='interval', default=interval, help='carrier loop interval, in ms (0 for default)')
parser.add_argument('-l', '--loglevel', dest='logLevel', default=logLevel, help='log level, 0-7')

args = parser.parse_args()

if args.libPath is not None:
   libPath = args.libPath

if args.logPath is not None:
   if args.logPath == '':
      logPath = None
   else:
      logPath = args.logPath

if args.dataPath is not None:
   if args.dataPath == '':
      persistentPath = None
   else:
      persistentPath = args.dataPath

if args.logLevel is not None:
   logLevel = args.logLevel

########################################################
# do something

# elastos bootstrap nodes
bootstraps = BootstrapNodes()
bootstraps.add(Bootstrap('13.58.208.50', '33445', '89vny8MrKdDKs7Uta9RdVmspPjnRMdwMmaiEW27pZ7gh'))
bootstraps.add(Bootstrap('18.216.102.47', '33445', 'G5z8MqiNDFTadFUPfMdYsYtkUDbX5mNCMVHMZtsCnFeb'))
bootstraps.add(Bootstrap('18.216.6.197', '33445', 'H8sqhRrQuJZ6iLtP2wanxt4LzdNrN2NNFnpPdq1uJ9n2'))
bootstraps.add(Bootstrap('52.83.171.135', '33445', '5tuHgK1Q4CYf4K5PutsEPK5E3Z7cbtEBdx7LwmdzqXHL'))
bootstraps.add(Bootstrap('52.83.191.228', '33445', '3khtxZo89SBScAMaHhTvD68pPHiKxgZT6hTCSZZVgNEm'))

# carrier options
opts = Options(
   udpEnabled = True,
   persistentLocation = persistentPath,
   bootstraps = bootstraps
)

# event callbacks

def idleCB(context):
    pass

def connectionStatusCB(status, context):
   cmd.printcb('connection state=' + status)

def readyCB(context):
   cmd.printcb('carrier state=ready')

def selfInfoCB(info, context):
   cmd.printcb('me:\n' + pformat(info))

def friendListCB(info, context):
   cmd.printcb('friend:\n' + pformat(info))

def friendsIterateCB(info, context):
   cmd.printcb('friends iterate:\n' + pformat(info))

def friendAddedCB(info, context):
   cmd.printcb('friend added:\n' + pformat(info))

def friendRemovedCB(id, context):
  cmd.printcb('friend removed:' + id)

def friendRequestCB(id, info, msg, context):
   cmd.printcb('friend request:' + id + '\n' + pformat(info) + '\n' + msg)

def friendInviteResponseCB(id, status, reason, data, bundle, context):
   # reason is null if status is 0
   cmd.printcb('friend invite response:' +  id + ' bundle=' + str(bundle) + ' status=' + status + ' reason=' + str(reason) + '\n' + data)

def friendConnectionCB(id, status, context):
   cmd.printcb('friend connection:' + id + ' status=' + status)

def friendInfoCB(id, info, context):
   cmd.printcb( 'friend info:' + id + '\n' + pformat(info))

def friendPresenceCB(id, presence, context):
   cmd.printcb('friend presence:' + id + ' presence=' + Presence[presence])

def friendMessageCB(id, msg, context):
  cmd.printcb('friend message:' + id + ' ' + msg)

def friendInviteCB(id, bundle, data, context):
   cmd.printcb('friend invite:' + id + ' bundle=' + str(bundle) + '\n' + data)

def groupInviteCB(id, cookie, context):
   cmd.printcb('group invite:' + id + ' cookie=' + cookie)

# start it up
session = None
carrier = Carrier(libPath, opts, threading=True, interval=interval)

if carrier.err.int:
   print 'Carrier creation failed.'
   print carrier.err.code
   print carrier.err.msg
   quit()
else:
   print 'Version', carrier.sdk.getVersion()
   print 'Address', carrier.getAddress()
   print 'Node ID', carrier.getNodeId()
   print 'User ID', carrier.getUserId() 

print

carrier.on('idle', idleCB)
carrier.on('connectionStatus', connectionStatusCB)
carrier.on('ready', readyCB)
carrier.on('selfInfo', selfInfoCB)
carrier.on('friendList', friendListCB)
carrier.on('friendsIterate', friendsIterateCB)
carrier.on('friendAdded', friendAddedCB)
carrier.on('friendRemoved', friendRemovedCB)
carrier.on('friendRequest', friendRequestCB)
carrier.on('friendInviteResponse', friendInviteResponseCB)
carrier.on('friendConnection', friendConnectionCB)
carrier.on('friendInfo', friendInfoCB)
carrier.on('friendPresence', friendPresenceCB)
carrier.on('friendMessage', friendMessageCB)
carrier.on('friendInvite', friendInviteCB)
carrier.on('groupInvite', groupInviteCB)

def printlog(msg):
   print msg
#carrier.initLog(7, None, printlog); 
carrier.initLog(logLevel, logPath, None); 

# run command prompt and carrier on threads; add threaded server for api

def signal_handler(sig, frame):
   print 'SIG killing...'
   raise SystemExit
signal.signal(signal.SIGINT, signal_handler)

cmd = CmdThread(carrier)
# somehow works...
try:
   carrier.run()
   cmd.run()
except SystemExit:
   print 'Killing carrier...'
   carrier.kill()
   sys.exit(0)   

