#!/usr/bin/python

from utils import Object
import threading
import ctypes, ctypes.util

from carrier_sdk import *

class Options(Object):

   def __init__(self, **kwargs):
      self.udpEnabled = False
      self.persistentLocation = ""
      self.bootstraps = []
      for k,v in kwargs.items():
         self[k] = v

class CarrierThread(threading.Thread):

   def __init__(self, carrier):
      super(CarrierThread, self).__init__()         
      self.carrier = carrier
   
   def run(self):
      self.carrier.sdk.run(self.carrier.interval)

   def done(self):
      print 'Carrier thread done.'
      self.carrier.sdk.kill()

class Carrier(Object):

   def __init__(self, libPath, opts=None, context=None, **kwargs):

      self.sdk = CarrierSdk(libPath)
      self.opts = opts
      self.interval = 0
      self.context = context
      self.threading = False
      self.quit = False

      for k,v in kwargs.items():
         self[k] = v

      self.on('idle', self.__idleCB__)
      if self.opts.bootstraps is None:
         self.opts.bootstraps = []
      if self.threading:
         self.thread = CarrierThread(self)

      self.elaCarrier = self.sdk.new(self.opts, self.context)

      self.err = self.sdk.getError()
      if self.err.int:
         self.elaCarrier = None

   def __idleCB__(self, context):
      if self.quit:
         self.kill()

   def getError(self):
      return self.sdk.getError()

   def on(self, event, cb):
      return self.sdk.callbacks.on(event, cb);

   def initLog(self, level, path, printer):
      return self.sdk.initLog(level, path, printer)

   def info(self):
      return self.sdk.getInfo()

   def run(self):
      self.quit = False
      if self.elaCarrier is not None:
         if self.threading:
            self.thread.start()
         else:
            self.sdk.run(self.interval)     

   def kill(self):
      self.quit = True
      if not self.threading:
         self.sdk.kill()
      else:
         self.thread.done()

   def getAddress(self):
      return self.sdk.getAddress()

   def getNodeId(self):
      return self.sdk.getNodeId()

   def getUserId(self):
      return self.sdk.getUserId()

   def getUserInfo(self):
      return self.sdk.getUserInfo()

   def setUserInfo(self, info):
      return self.sdk.setUserInfo(info)

   def getPresence(self):
      return self.sdk.getPresence()

   def setPresence(self, presence):
      return self.sdk.setPresence(presence)

   def getFriends(self, context=None):
      return self.sdk.getFriends(context)

   def getFriendInfo(self, id):
      return self.sdk.getFriendInfo(id)

   def addFriend(self, address, msg):
      return self.sdk.addFriend(address, msg)

   def labelFriend(self, id, label):
      return self.sdk.labelFriend(id, label)

   def sendMsg(self, id, msg):
      return self.sdk.sendMsg(id, msg)      

   def acceptFriend(self, id):
      return self.sdk.acceptFriend(id)

   def removeFriend(self, id):
      return self.sdk.removeFriend(id)

   def isFriend(self, id):
      return self.sdk.isFriend(id)

   def inviteFriend(self, id, data, bundle=None, context=None):
      return self.sdk.inviteFriend(id, data, bundle, context)

   def replyFriendInvite(self, id, status, reason, data, bundle=None):
      status = int(status)
      return self.sdk.replyFriendInvite(id, status, reason, data, bundle)

# higher-level stuff
# add lookup for nickname, name, etc for userid
# monitor related callbacks and update Friends array
# connection lists, etc.
class Friend():

   def __init__(self, **kwargs):

      for k,v in kwargs.items():
         self[k] = v

class Friends():

   def __init__(self, **kwargs):
      self.friends = []
      for k,v in kwargs.items():
         self[k] = v

   def add(self, friend):
      self.friends.append(friend)   # check for dups, etc.