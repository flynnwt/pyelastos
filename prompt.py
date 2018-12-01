import sys, traceback
from pprint import pprint, pformat
import threading
import time

from cmd import Cmd
import colorama
from colorama import Fore, Back, Style
colorama.init()

class MyPrompt(Cmd, object):

   def __init__(self, cmd, **kwargs):
     super(MyPrompt, self).__init__()     
     self.cmd = cmd
     self.context = None 
     for k,v in kwargs.items():
         self[k] = v

   def __setitem__(self, k, v):
      self.__setattr__(k, v)

   def do_address(self, args):
      """get address\naddress"""
      self.cmd.printresp(self.carrier.getAddress())

   def do_nodeid(self, args):
      """get node ID\nodeid"""
      self.cmd.printresp(self.carrier.getNodeId())

   def do_userid(self, args):
      """get user ID\nuserid"""
      self.cmd.printresp(self.carrier.getUserId())
   
   def do_info(self, args):
      """info\nraw carrier info"""
      self.cmd.printresp(pformat(self.carrier.info()))

   def do_userinfo(self, args):
      """get/set user info\nuserinfo [k=v,..]; for set, specify parms as key=value, comma-separated"""
      info = self.carrier.getUserInfo()
      if len(args) == 0:
         self.cmd.printresp(pformat(info))
         return
      if info is not None:
         tokens = args.split(',')
         for i in range(0, len(tokens)):
            kv = tokens[i].split('=')
            k = kv[0]
            if len(kv) != 2:
               self.cmd.printerr('Bad spec <' + tokens[i] + '>')
               return
            else:
               info[k] = kv[1]
         rc = self.carrier.setUserInfo(info)   
         if not self.cmd.checkrc(rc):
            self.cmd.printresp(pformat(self.carrier.getUserInfo()))
   
   def do_presence(self, args):
      """get/set user presence\npresence [mode]; for set, specify none|away|busy"""
      if len(args) == 0:
         self.cmd.printresp(self.carrier.getPresence())
      else:
         if self.carrier.setPresence(args):
            print 'Failed'
         else:
            self.cmd.printresp(self.carrier.getPresence())

   def do_getfriends(self, args):
      """get friends list\ngetfriends"""
      self.carrier.getFriends(self.context)

   def do_addfriend(self, args):
      """add a friend\naddfriend address,msg"""
      tokens = args.split(',')
      if len(tokens) < 2:
         self.cmd.printerr('Need address,msg')
      else:
         addr = tokens[0]
         msg = ','.join(tokens[1:])
         rc = self.carrier.addFriend(addr, msg)
         self.cmd.checkrc(rc)

   def do_friendinfo(self, args):
      """get friend info\nfriendinfo id"""
      if len(args) == 0:
         self.cmd.printerr('Need ID')
      else:
         rc = self.cmd.printresp(pformat(self.carrier.getFriendInfo(args)))
         self.cmd.checkrc(rc)

   def do_labelfriend(self, args):
      """add label to friend\nlabelfriend id,msg"""
      tokens = args.split(',')
      if len(tokens) < 2:
         self.cmd.printerr('Need ID,msg')
      else:
         id = tokens[0]
         label = ','.join(tokens[1:])
         rc = self.carrier.labelFriend(id, label)
         self.cmd.checkrc(rc)

   def do_msg(self, args):
      """send msg\nmsg id,msg"""
      tokens = args.split(',')
      if len(tokens) < 2:
         self.cmd.printerr('Need ID,msg')
      else:
         id = tokens[0]
         msg = ','.join(tokens[1:])
         rc = self.carrier.sendMsg(id, msg)
         self.cmd.checkrc(rc)

   def do_acceptfriend(self, args):
      """accept friend request\nacceptfriend id"""
      if len(args) == 0:
         self.cmd.printerr('Need ID')
      else:
         rc = self.carrier.acceptFriend(args)
         self.cmd.checkrc(rc)

   def do_removefriend(self, args):
      """remove friend\nremovefriend id"""
      if len(args) == 0:
         self.cmd.printerr('Need ID')
      else:      
         rc = self.carrier.removeFriend(args)
         self.cmd.checkrc(rc)

   def do_isfriend(self, args):
      """check if friend\nisfriend id"""
      if len(args) == 0:
         self.cmd.printerr('Need ID')
      else:      
         self.cmd.printresp('yes' if self.carrier.isFriend(args) else 'no')

   def do_invitefriend(self, args):
      """invite friend (app)\ninvitefriend id,data,[bundle],[context]"""
      tokens = args.split(',')
      if len(tokens) < 2:
         self.cmd.printerr('Need ID,data,[bundle],[context]')
      else:
         id = tokens[0]
         data = tokens[1]
         bundle = None if len(tokens) < 3 else tokens[2]
         context = None if len(tokens) < 4 else tokens[3]
         rc = self.carrier.inviteFriend(id, data, bundle, context)
         self.cmd.checkrc(rc)

   def do_replyfriendinvite(self, args):
      """reply to friend invite (app)\ninvitefriend id,status,reason,data,[bundle]"""
      tokens = args.split(',')
      if len(tokens) < 4:
         self.cmd.printerr('Need ID,status,reason,data,[bundle]')
      else:
         id = tokens[0]
         status = tokens[1]
         reason = tokens[2]
         data = tokens[3]
         bundle = None if len(tokens) < 5 else tokens[4]
         rc = self.carrier.replyFriendInvite(id, status, reason, data, bundle) # int(status)?
         self.cmd.checkrc(rc)

   def do_quit(self, args):
        """quit"""
        raise SystemExit

class CmdThread(threading.Thread):

   def __init__(self, carrier, **kwargs):
      super(CmdThread, self).__init__()  
      self.carrier = carrier
      self.sep = Fore.YELLOW + '-' * 20
      self.cmdColor = Fore.GREEN
      self.cbColor = Fore.YELLOW
      self.respColor = Fore.CYAN
      self.errColor = Fore.RED
      #self.reset = Style.RESET_ALL
      self.reset = self.cmdColor

      for k,v in kwargs.items():
         self[k] = v

      self.cmd = MyPrompt(self, carrier=self.carrier)
      self.cmd.prompt = self.cmdColor + '> '
      self.cmd.default = self.__default__

   def __default__(self, line):
      self.printerr('*** Unknown syntax: ' + line)      

   def run(self):
      try:
         self.cmd.cmdloop('Starting command interpreter...')             
      except Exception as e:
         print e
         exc_type, exc_value, exc_traceback = sys.exc_info()         
         traceback.print_tb(exc_traceback)   
         raise SystemExit
      except BaseException as e:
         print 'CmdThread exiting...'
         raise SystemExit

   def printcb(self, msg):
      print self.sep
      print self.cbColor + msg, self.reset 

   def printresp(self, msg):
      print self.respColor + msg, self.reset       

   def printerr(self, msg):
      print self.errColor + msg, self.reset
      
   def checkrc(self, rc):
     if rc != 0:
       elaerr = self.carrier.getError()
       self.printerr('rc=' + str(rc) + ' elaerr=' + elaerr.code + ' ' + elaerr.msg)
     return rc