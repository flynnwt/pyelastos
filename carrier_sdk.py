#!/usr/bin/python

import os, ctypes, ctypes.util
from pprint import pprint

from utils import Object, Enum

# not using right now; and need to do differently for win anyway
clib = ctypes.CDLL(ctypes.util.find_library('c'))
try:
  snprintf = clib.snprintf
  snprintf.restype = ctypes.c_int
  snprintf.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_char_p]
except:
  snprintf = None

class ElaErrorGroups(Object):

   ELAF_GENERAL = 0x01
   ELAF_SYS = 0x02
   ELAF_RESERVED1 = 0x03
   ELAF_RESERVED2 = 0x04
   ELAF_ICE = 0x05
   ELAF_DHT = 0x06

   def __init__(self):
      for k in ElaErrors.__dict__:
         v = ElaErrors.__dict__[k]
         if isinstance(v,  (int, long)):
            self[v] = k
            self[k] = v

class ElaErrors(Object):
   
   ELASUCCESS = 0

   ELAERR_INVALID_ARGS = 0x01
   ELAERR_OUT_OF_MEMORY = 0x02
   ELAERR_BUFFER_TOO_SMALL = 0x03
   ELAERR_BAD_PERSISTENT_DATA = 0x04
   ELAERR_INVALID_PERSISTENCE_FILE = 0x05
   ELAERR_INVALID_CONTROL_PACKET = 0x06
   ELAERR_INVALID_CREDENTIAL = 0x07
   ELAERR_ALREADY_RUN = 0x08
   ELAERR_NOT_READY = 0x09
   ELAERR_NOT_EXIST = 0x0A
   ELAERR_ALREADY_EXIST = 0x0B
   ELAERR_NO_MATCHED_REQUEST = 0x0C
   ELAERR_INVALID_USERID = 0x0D
   ELAERR_INVALID_NODEID = 0x0E
   ELAERR_WRONG_STATE = 0x0F
   ELAERR_BUSY = 0x10
   ELAERR_LANGUAGE_BINDING = 0x11
   ELAERR_ENCRYPT = 0x12
   ELAERR_SDP_TOO_LONG = 0x13
   ELAERR_INVALID_SDP = 0x14
   ELAERR_NOT_IMPLEMENTED = 0x15
   ELAERR_LIMIT_EXCEEDED = 0x16
   ELAERR_PORT_ALLOC = 0x17
   ELAERR_BAD_PROXY_TYPE = 0x18
   ELAERR_BAD_PROXY_HOST = 0x19
   ELAERR_BAD_PROXY_PORT = 0x1A
   ELAERR_PROXY_NOT_AVAILABLE = 0x1B
   ELAERR_ENCRYPTED_PERSISTENT_DATA = 0x1C
   ELAERR_BAD_BOOTSTRAP_HOST = 0x1D
   ELAERR_BAD_BOOTSTRAP_PORT = 0x1E
   ELAERR_TOO_LONG = 0x1F
   ELAERR_ADD_SELF = 0x20
   ELAERR_BAD_ADDRESS = 0x21
   ELAERR_FRIEND_OFFLINE = 0x22
   ELAERR_UNKNOWN = 0xFF

   def ELA_MK_ERROR(self, facility, code):
      return 0x80000000 | ((facility) << 24) | (((code) & 0x80000000) >> 8) | ((code) & 0x7FFFFFFF)

   def ELA_GENERAL_ERROR(self, code):
      return self.ELA_MK_ERROR(ElaErrorGroups.ELAF_GENERAL, code)
   
   def ELA_SYS_ERROR(self, code):
      return self.ELA_MK_ERROR(ElaErrorGroups.ELAF_SYS, code)
   
   def ELA_ICE_ERROR(self, code):
      return self.ELA_MK_ERROR(ElaErrorGroups.ELAF_ICE, code)
   
   def ELA_DHT_ERROR(self, code):
      return self.ELA_MK_ERROR(ElaErrorGroups.ELAF_DHT, code)

   def __init__(self):
      for k in ElaErrors.__dict__:
         v = ElaErrors.__dict__[k]
         if isinstance(v,  (int, long)):
            self[v] = k
            self[k] = v

   def hex(self, v):
      return '{0:08X}'.format(v)
      
NONE = 0
AWAY = 1
BUSY = 2
Presence = Enum(none=NONE, away=AWAY, busy=BUSY)

CONNECTED = 0
DISCONNECTED = 1
ConnectionState = Enum(connected=CONNECTED, disconnected=DISCONNECTED)

FATAL = 1
ERROR = 2
WARNING = 3
INFO = 4
DEBUG = 5
TRACE = 6
VERBOSE = 7
LogLevel = Enum(none=NONE, fatal=FATAL, warning=WARNING, info=INFO, debug=DEBUG, trace=TRACE, verbose=VERBOSE)

DHT_PUBLIC_KEY_SIZE = 32
DHT_ADDRESS_SIZE = 32 + ctypes.sizeof(ctypes.c_uint) + ctypes.sizeof(ctypes.c_uint8)*2

ELA_MAX_ADDRESS_LEN = 52
ELA_MAX_ID_LEN = 45
ELA_MAX_USER_NAME_LEN = 63
ELA_MAX_USER_DESCRIPTION_LEN = 127
ELA_MAX_PHONE_LEN = 31
ELA_MAX_EMAIL_LEN = 127
ELA_MAX_REGION_LEN = 127
ELA_MAX_GENDER_LEN = 31
ELA_MAX_NODE_DESCRIPTION_LEN = 127
ELA_MAX_NODE_NAME_LEN = 63
ELA_MAX_APP_MESSAGE_LEN = 1024
ELA_MAX_INVITE_DATA_LEN = 8192
ELA_MAX_BUNDLE_LEN = 511
ELA_MAX_INVITE_REPLY_REASON_LEN = 255
ELA_MAX_GROUP_TITLE_LEN = 127

ELA_STATUS_TIMEOUT = 1

def printlog(format, *args):
   print "printlog", format, args

ELALOGLEVEL = ctypes.c_int;
ELAPRESENCESTATUS = ctypes.c_int;
ELACONNECTIONSTATUS = ctypes.c_int;

# not sure if there's a correct way to do va_list
ELAPRINTLOG = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p)

class DHT(ctypes.Structure):
   _fields_ = [
      ('padding', ctypes.c_char * 32)
   ]     

# void (*notify_connection)(bool connected, void *context);
# void (*notify_friend_desc)(uint32_t friend_number, const uint8_t *desc, size_t length, void *context);
# void (*notify_friend_connection)(uint32_t friend_number, bool connected, void *context);
# void (*notify_friend_status)(uint32_t friend_number, int status, void *context);
# void (*notify_friend_request)(const uint8_t *public_key, const uint8_t *hello, size_t len, void *context);
# void (*notify_friend_message)(uint32_t friend_number, const uint8_t *message, size_t length, void *context);
# void (*notify_group_invite)(uint32_t fnum, const uint8_t *cookie, size_t len, void *context);
# void (*notify_group_connected)(uint32_t gnum, void *context);
# void (*notify_group_message)(uint32_t gnum, uint32_t pnum, const uint8_t *msg, size_t len, void *context);
# void (*notify_group_title)(uint32_t gnum, uint32_t pnum, const char *title, void *context);
# void (*notify_group_peer_name)(uint32_t gnum, uint32_t pnum, const char *name, void *context);
# void (*notify_group_peer_list_changed)(uint32_t gnum, void *context);
class DHTCALLBACKS(ctypes.Structure):
   _fields_ = [
      ('context', ctypes.c_void_p),
      ('notify_connection', ctypes.CFUNCTYPE(None)),
      ('notify_friend_desc', ctypes.CFUNCTYPE(None)),
      ('notify_friend_connection', ctypes.CFUNCTYPE(None)),
      ('notify_friend_status', ctypes.CFUNCTYPE(None)),
      ('notify_friend_request', ctypes.CFUNCTYPE(None)),
      ('notify_friend_message', ctypes.CFUNCTYPE(None)),
      ('notify_group_invite', ctypes.CFUNCTYPE(None)),
      ('notify_group_connected', ctypes.CFUNCTYPE(None)),
      ('notify_group_message', ctypes.CFUNCTYPE(None)),
      ('notify_group_title', ctypes.CFUNCTYPE(None)),
      ('notify_group_peer_name', ctypes.CFUNCTYPE(None)),
      ('notify_group_peer_list_changed', ctypes.CFUNCTYPE(None)),
   ]

class ELABOOTSTRAPNODE(ctypes.Structure):
   _fields_ = [
      ('ipv4', ctypes.c_char_p),   
      ('ipv6', ctypes.c_char_p),   
      ('port', ctypes.c_char_p),   
      ('public_key', ctypes.c_char_p)
   ]  

   def __init__(self):
      super(ctypes.Structure, self).__init__()
      self.ipv4 = ''
      self.ipv6 = ''
      self.port = ''
      self.public_key = ''

class PREFERENCES(ctypes.Structure):
   _fields_ = [
      ('data_location', ctypes.c_char_p),
      ('udp_enabled', ctypes.c_bool),
      ('bootstraps_size', ctypes.c_int),
      ('bootstraps', ctypes.POINTER(ELABOOTSTRAPNODE))
   ]

class ELAUSERINFO(ctypes.Structure):
   _fields_ = [
      ('userid', ctypes.c_char * (ELA_MAX_ID_LEN + 1)),
      ('name', ctypes.c_char * (ELA_MAX_USER_NAME_LEN + 1)),
      ('description', ctypes.c_char * (ELA_MAX_USER_DESCRIPTION_LEN + 1)),
      ('has_avatar', ctypes.c_int),
      ('gender', ctypes.c_char * (ELA_MAX_GENDER_LEN + 1)),
      ('phone', ctypes.c_char * (ELA_MAX_PHONE_LEN + 1)),
      ('email', ctypes.c_char * (ELA_MAX_EMAIL_LEN + 1)),
      ('region', ctypes.c_char * (ELA_MAX_REGION_LEN + 1))
   ]

class ELAFRIENDINFO(ctypes.Structure):
   _fields_ = [
      ('user_info', ELAUSERINFO),
      ('label', ctypes.c_char * (ELA_MAX_USER_NAME_LEN + 1)),
      ('status', ELACONNECTIONSTATUS),
      ('presence', ELAPRESENCESTATUS),
   ]

SESSION = ctypes.c_void_p    

# blackbox
SIZEOF_PTHREAD_MUTEX_T = 40
class PTHREAD_MUTEX_T(ctypes.Union):
   _fields_ = [('dummy', ctypes.c_char * SIZEOF_PTHREAD_MUTEX_T)]

PTHREAD_T = ctypes.c_ulong

LIST_T = ctypes.c_void_p
HASHTABLE_T = ctypes.c_void_p;                                               

class ELAOPTIONS(ctypes.Structure):
   _fields_ = [
      ('persistent_location', ctypes.c_char_p),
      ('udp_enabled', ctypes.c_bool),
      ('bootstraps_size', ctypes.c_size_t),
      ('bootstraps', ctypes.POINTER(ELABOOTSTRAPNODE))
   ]

   def __init__(self):
      super(ctypes.Structure, self).__init__()
      self.persistent_location = ''
      self.udp_enabled = False
      self.bootstraps_size = 0
      self.bootstraps = None

# circ ref
class ELACARRIER(ctypes.Structure):
   pass

# void (*group_connected)(ElaCarrier *carrier, const char *groupid, void *context);
# void (*group_message)(ElaCarrier *carrier, const char *groupid, const char *from, const void *message, size_t length, void *context);
# void (*group_title)(ElaCarrier *carrier, const char *groupid, const char *from, const char *title, void *context);
# void (*peer_name)(ElaCarrier *carrier, const char *groupid, const char *peerid, const char *peer_name, void *context);
# void (*peer_list_changed)(ElaCarrier *carrier, const char *groupid, void *context);

class ELAGROUPCALLBACKS(ctypes.Structure):
   _fields_ = [
      ('group_connected', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_void_p)),
      ('group_message', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)),
      ('group_title', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p)),
      ('peer_name', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p)),
      ('peer_list', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_void_p))
   ] 

# void (*idle)(ElaCarrier *carrier, void *context);
# void (*connection_status)(ElaCarrier *carrier, ElaConnectionStatus status, void *context);
# void (*ready)(ElaCarrier *carrier, void *context);
# void (*self_info)(ElaCarrier *carrier, const ElaUserInfo *info, void *context);
# bool (*friend_list)(ElaCarrier *carrier, const ElaFriendInfo* info, void* context);
# void (*friend_connection)(ElaCarrier *carrier,const char *friendid, ElaConnectionStatus status, void *context);
# void (*friend_info)(ElaCarrier *carrier, const char *friendid, const ElaFriendInfo *info, void *context);
# void (*friend_presence)(ElaCarrier *carrier, const char *friendid, ElaPresenceStatus presence, void *context);
# void (*friend_request)(ElaCarrier *carrier, const char *userid, const ElaUserInfo *info, const char *hello, void *context);
# void (*friend_added)(ElaCarrier *carrier, const ElaFriendInfo *info, void *context);
# void (*friend_removed)(ElaCarrier *carrier, const char *friendid, void *context);
# void (*friend_message)(ElaCarrier *carrier, const char *from, const void *msg, size_t len, void *context);
# void (*friend_invite)(ElaCarrier *carrier, const char *from, const char *bundle, const void *data, size_t len, void *context);
# void (*group_invite)(ElaCarrier *w, const char *from, const void *cookie, size_t len, void *context);
class ELACALLBACKS(ctypes.Structure):
   _fields_ = [
      ('idle', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_void_p)),
      ('connection_status', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ELACONNECTIONSTATUS, ctypes.c_void_p)),
      ('ready', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_void_p)),
      ('self_info', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAUSERINFO), ctypes.c_void_p)),
      ('friend_list', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAFRIENDINFO), ctypes.c_void_p)),
      ('friend_connection', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ELACONNECTIONSTATUS, ctypes.c_void_p)),
      ('friend_info', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.POINTER(ELAFRIENDINFO), ctypes.c_void_p)),
      ('friend_presence', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ELAPRESENCESTATUS, ctypes.c_void_p)),
      ('friend_request', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.POINTER(ELAUSERINFO), ctypes.c_char_p,  ctypes.c_void_p)),
      ('friend_added', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAUSERINFO), ctypes.c_void_p)),
      ('friend_removed', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_void_p)),
      ('friend_message', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)),
      ('friend_invite', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)),
      ('group_invite', ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)),
      ('group_callbacks', ELAGROUPCALLBACKS)
   ] 

ELACARRIER._fields_ = [
      ('ext_mutex', PTHREAD_MUTEX_T),
      ('session', SESSION),
      ('dht', DHT),
      ('pref', PREFERENCES),
      ('public_key', ctypes.c_char * DHT_PUBLIC_KEY_SIZE),
      ('address', ctypes.c_char * DHT_ADDRESS_SIZE),
      ('base58_addr', ctypes.c_char * (ELA_MAX_ADDRESS_LEN + 1)),
      ('me', ELAUSERINFO),
      ('presence_status', ELAPRESENCESTATUS),
      ('connection_status', ELACONNECTIONSTATUS),
      ('is_ready', ctypes.c_bool),
      ('callbacks', ELACALLBACKS),   
      ('group_callbacks', ELAGROUPCALLBACKS),  
      ('context', ctypes.c_void_p),
      ('dht_callbacks', DHTCALLBACKS),
      ('friend_events', ctypes.POINTER(LIST_T)),
      ('friends', ctypes.POINTER(HASHTABLE_T)),
      ('tcallbacks', ctypes.POINTER(HASHTABLE_T)),
      ('thistory', ctypes.POINTER(HASHTABLE_T)),
      ('tassemblyireqs', ctypes.POINTER(HASHTABLE_T)),
      ('tassemblyirsps', ctypes.POINTER(HASHTABLE_T)),
      ('main_thread', PTHREAD_T),
      ('running', ctypes.c_int),
      ('quit', ctypes.c_int)     
   ]

# bool ElaFriendsIterateCallback(const ElaFriendInfo *info, void *context)
ELAFRIENDSITERATECALLBACK = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ELAFRIENDINFO), ctypes.c_void_p)
# void ElaFriendInviteResponseCallback(ElaCarrier *carrier, const char *from, const char *bundle, int status, const char *reason, const void *data, size_t len, void *context)
ELAFRIENDINVITERESPONSECALLBACK = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)

errors = ElaErrors()
class Error(Object):
   def __init__(self, n=0):
      self.int = n
      self.code = '{0:08X}'.format(n)
      self.msg = errors[n & 0x00FFFFFF]

def __createElaCarrierInterfaces__(lib):

   # Carrier
   # ElaCarrier *ela_new(const ElaOptions *options, ElaCallbacks *callbacks, void *context)
   lib.ela_new.restype = ctypes.POINTER(ELACARRIER);
   lib.ela_new.argtypes = [ctypes.POINTER(ELAOPTIONS), ctypes.POINTER(ELACALLBACKS), ctypes.POINTER(ctypes.c_void_p)]
   # int ela_run(ElaCarrier *carrier, int interval)
   lib.ela_run.restype = ctypes.c_int
   lib.ela_run.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_int]
   # void ela_kill(ElaCarrier *carrier)
   lib.ela_kill.restypes = None
   lib.ela_kill.argtypes = [ctypes.POINTER(ELACARRIER)]
   # bool ela_is_ready(ElaCarrier *carrier)
   lib.ela_is_ready.restype = ctypes.c_bool
   lib.ela_is_ready.argtypes = [ctypes.POINTER(ELACARRIER)]

   # Node
   # char *ela_get_address(ElaCarrier *carrier, char *address, size_t len)
   lib.ela_get_address.restype = ctypes.c_char_p
   lib.ela_get_address.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_size_t]
   # char *ela_get_nodeid(ElaCarrier *carrier, char *nodeid, size_t len)
   lib.ela_get_nodeid.restype = ctypes.c_char_p
   lib.ela_get_nodeid.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_size_t]
   # char *ela_get_userid(ElaCarrier *carrier, char *userid, size_t len)
   lib.ela_get_userid.restype = ctypes.c_char_p
   lib.ela_get_userid.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_size_t]
   #char *ela_get_id_by_address(const char *address, char *userid, size_t len)
   lib.ela_get_id_by_address.restype = ctypes.c_char_p
   lib.ela_get_id_by_address.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
   # int ela_set_self_nospam(ElaCarrier *carrier, uint32_t nospam)
   lib.ela_set_self_nospam.restype = ctypes.c_int
   lib.ela_set_self_nospam.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_uint32]
   # int ela_get_self_nospam(ElaCarrier *carrier, uint32_t *nospam)
   lib.ela_get_self_nospam.restype = ctypes.c_int
   lib.ela_get_self_nospam.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.POINTER(ctypes.c_uint32)]
   #int ela_set_self_info(ElaCarrier *carrier, const ElaUserInfo *info)
   lib.ela_set_self_info.restype = ctypes.c_int
   lib.ela_set_self_info.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAUSERINFO)]
   #int ela_get_self_info(ElaCarrier *carrier, ElaUserInfo *info)
   lib.ela_get_self_info.restype = ctypes.c_int
   lib.ela_get_self_info.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAUSERINFO)] 
   # int ela_set_self_presence(ElaCarrier *carrier, ElaPresenceStatus presence)
   lib.ela_set_self_presence.restype = ctypes.c_int
   lib.ela_set_self_presence.argtypes = [ctypes.POINTER(ELACARRIER), ELAPRESENCESTATUS]
   # int ela_get_self_presence(ElaCarrier *carrier, ElaPresenceStatus *presence)
   lib.ela_get_self_presence.restype = ctypes.c_int
   lib.ela_get_self_presence.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAPRESENCESTATUS)]

   # Friends
   #int ela_get_friends(ElaCarrier *carrier, ElaFriendsIterateCallback *callback, void *context)
   # ***why not directly called through w->callbacks? why diff than friend_list cb????
   lib.ela_get_friends.restype = ctypes.c_int
   lib.ela_get_friends.argtypes = [ctypes.POINTER(ELACARRIER), ELAFRIENDSITERATECALLBACK, ctypes.c_void_p]
   # int ela_get_friend_info(ElaCarrier *carrier, const char *friendid, ElaFriendInfo *info)
   lib.ela_get_friend_info.restype = ctypes.c_int
   lib.ela_get_friend_info.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.POINTER(ELAFRIENDINFO)]
   # int ela_set_friend_label(ElaCarrier *carrier, const char *friendid, const char *label)
   lib.ela_set_friend_label.restype = ctypes.c_int
   lib.ela_set_friend_label.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p]
   # bool ela_is_friend(ElaCarrier *carrier, const char *userid)
   lib.ela_is_friend.restype = ctypes.c_bool
   lib.ela_is_friend.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p]
   # int ela_add_friend(ElaCarrier *carrier, const char *address, const char *hello)
   lib.ela_add_friend.restype = ctypes.c_int
   lib.ela_add_friend.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p]
   # int ela_accept_friend(ElaCarrier *carrier, const char *userid)
   lib.ela_accept_friend.restype = ctypes.c_int
   lib.ela_accept_friend.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p]
   # int ela_remove_friend(ElaCarrier *carrier, const char *userid)
   lib.ela_remove_friend.restype = ctypes.c_int
   lib.ela_remove_friend.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p]
   # int ela_send_friend_message(ElaCarrier *carrier, const char *to, const void *msg, size_t len)
   lib.ela_send_friend_message.restype = ctypes.c_int
   lib.ela_send_friend_message.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
   # int ela_invite_friend(ElaCarrier *carrier, const char *to, const char *bundle, const void *data, size_t len, ElaFriendInviteResponseCallback *callback, void *context)
   lib.ela_invite_friend.restype = ctypes.c_int
   lib.ela_invite_friend.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ELAFRIENDINVITERESPONSECALLBACK, ctypes.c_void_p]
   # int ela_reply_friend_invite(ElaCarrier *carrier, const char *to, const char *bundle, int status, const char *reason, const void *data, size_t len)
   lib.ela_reply_friend_invite.restype = ctypes.c_int
   lib.ela_reply_friend_invite.argtypes = [ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
 
   # Utils
   # const char *ela_get_version(void)
   lib.ela_get_version.restype = ctypes.c_char_p
   lib.ela_get_version.argtypes = None
   # void ela_log_init(ElaLogLevel level, const char *log_file, void (*log_printer)(const char *format, va_list args))
   lib.ela_log_init.restype = None
   lib.ela_log_init.argtypes = [ctypes.c_int, ctypes.c_char_p, ELAPRINTLOG]
   # bool ela_address_is_valid(const char *address)
   lib.ela_address_is_valid.restype = ctypes.c_int
   lib.ela_address_is_valid.argtypes = [ctypes.c_char_p]
   # bool ela_id_is_valid(const char *id)
   lib.ela_id_is_valid.restype = ctypes.c_bool
   lib.ela_id_is_valid.argtypes = [ctypes.c_char_p]
   # int ela_get_error(void)
   lib.ela_get_error.restype = ctypes.c_uint
   lib.ela_get_error.argtypes = None
   # void ela_clear_error(void)
   lib.ela_clear_error.restype = None
   lib.ela_clear_error.argtypes = None

class Bootstrap(Object):
 
   def __init__(self, ipv4=None, port=None, publicKey=None, ipv6=None):
      self.ipv4 = ipv4
      self.ipv6 = ipv6
      self.port = port
      self.publicKey = publicKey

class BootstrapNodes(Object):

   def __init__(self):
      self.nodes = []

   def add(self, node):
      self.nodes.append(node)

   def len(self):
      return len(self.nodes)

   def get_ela(self):
      BOOTSTRAPARRAY = ELABOOTSTRAPNODE * len(self.nodes)
      bootstraps = BOOTSTRAPARRAY()
      for i in range(0, len(self.nodes)):
         bootstraps[i].ipv4 = self.nodes[i].ipv4
         bootstraps[i].ipv6 = self.nodes[i].ipv6
         bootstraps[i].port = self.nodes[i].port
         bootstraps[i].public_key = self.nodes[i].publicKey
      return bootstraps

class UserInfo(Object):   

   def __init__(self, ela=None):
      self.userid = None
      self.name = None
      self.description = None
      self.hasAvatar = False
      self.gender = None
      self.phone = None
      self.email = None
      self.region = None
      if ela is not None:
         self.set(ela)

   def set(self, ela):
      self.userid = ela.userid
      self.name = ela.name
      self.description = ela.description
      self.hasAvatar = ela.has_avatar
      self.gender = ela.gender
      self.phone = ela.phone
      self.email = ela.email
      self.region = ela.region      

# needs to limit to max_lens? does ctypes check if a len is spec'd in ELAUSERINFO?
   def get_ela(self):
      ela = ELAUSERINFO()
      ela.userid = self.userid
      ela.name = self.name
      ela.description = self.description
      ela.has_avatar = self.hasAvatar
      ela.gender = self.gender
      ela.phone = self.phone
      ela.email = self.email
      ela.region = self.region
      return ela

class FriendInfo(Object):

   def __init__(self, ela=None):
      self.userInfo = UserInfo()
      self.label = ''
      self.status = None
      self.presence = None
      if ela is not None:
         self.set(ela)

   def set(self, ela):
      self.userInfo = UserInfo(ela.user_info)
      self.label = ela.label
      self.status = ConnectionState[ela.status]
      self.presence = Presence[ela.presence]

   def get_ela(self):
      ela = ELAFRIENDINFO()
      ela.label = self.label
      ela.status = ConnectionState[self.status]
      ela.presence = Presence[ela.presence]
      ela.user_info = self.userInfo.get_ela()

class Callbacks(Object):

   def __init__(self, carrier = None):

      self.events = Object()
      self.elaCallbacks = ELACALLBACKS()
      
      self.events.idle = []
      self.elaCallbacks.idle = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_void_p)(self.__idleCB__)
  
      self.events.connectionStatus = []
      self.elaCallbacks.connection_status = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ELACONNECTIONSTATUS, ctypes.c_void_p)(self.__connectionStatusCB__)

      self.events.ready = []
      self.elaCallbacks.ready = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_void_p)(self.__readyCB__)

      self.events.selfInfo = []
      self.elaCallbacks.self_info = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAUSERINFO), ctypes.c_void_p)(self.__selfInfoCB__)
      
      self.events.friendList = []
      self.elaCallbacks.friend_list = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAFRIENDINFO), ctypes.c_void_p)(self.__friendListCB__)
      
      self.events.friendConnection = []
      self.elaCallbacks.friend_connection = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ELACONNECTIONSTATUS, ctypes.c_void_p)(self.__friendConnectionCB__)
      
      self.events.friendInfo = []
      self.elaCallbacks.friend_info = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.POINTER(ELAFRIENDINFO), ctypes.c_void_p)(self.__friendInfoCB__)

      self.events.friendPresence = []
      self.elaCallbacks.friend_presence = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ELAPRESENCESTATUS, ctypes.c_void_p)(self.__friendPresenceCB__)
 
      self.events.friendRequest = []
      self.elaCallbacks.friend_request = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.POINTER(ELAUSERINFO), ctypes.c_char_p,  ctypes.c_void_p)(self.__friendRequestCB__)

      self.events.friendAdded = []
      self.elaCallbacks.friend_added = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.POINTER(ELAUSERINFO), ctypes.c_void_p)(self.__friendAddedCB__)
    
      self.events.friendRemoved = []
      self.elaCallbacks.friend_removed = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_void_p)(self.__friendRemovedCB__)

      self.events.friendMessage = []
      self.elaCallbacks.friend_message = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)(self.__friendMessageCB__)

      self.events.friendInvite = []
      self.elaCallbacks.friend_invite = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)(self.__friendInviteCB__)

      self.events.groupInvite = []  
      self.elaCallbacks.group_invite = ctypes.CFUNCTYPE(None, ctypes.POINTER(ELACARRIER), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p)(self.__groupInviteCB__)

      self.events.friendsIterate = []
      self.friendsIterate = ELAFRIENDSITERATECALLBACK(self.__friendsIterateCB__)

      self.events.friendInviteResponse = []
      self.friendInviteResponse = ELAFRIENDINVITERESPONSECALLBACK(self.__friendInviteResponseCB__)

   def on(self, event, cb):
      self.events[event].append(cb)
      return len(self.events[event]) - 1

   def remove(self, event, id):
      new = []
      for i in range(0, len(self.events[event])):
         if i != id:
            new.append(self.events[event][i])
      self.events[event] = new

   # these are called by C - not sure why this even works as methods instead of functions outside the class
   def __idleCB__(self, carrier, context):
      cb = self.events.idle
      for i in range(0, len(cb)):
         (cb[i])(context)

   def __connectionStatusCB__(self, carrier, status, context):
      #print 'called connectionStatusCB handler', status
      cb = self.events.connectionStatus
      for i in range(0, len(cb)):
         (cb[i])(ConnectionState[status], context)

   def __readyCB__(self, carrier, context):
      #print 'called readyCB handler'
      cb = self.events.ready
      for i in range(0, len(cb)):
         (cb[i])(context)

   # This callback is reserved for future compatibility.
   def __selfInfoCB__(self, carrier, info, context):
      print 'called selfInfoCB handler'
      cb = self.events.selfInfo
      if info:
         info = UserInfo(info.contents)
      else:
         info = None
      for i in range(0, len(cb)):
         (cb[i])(info, context)

   def __friendListCB__(self, carrier, info, context):
      #print 'called friendListCB handler'
      cb = self.events.friendList
      if info:
         info = FriendInfo(info.contents)
      else:
         info = None
      for i in range(0, len(cb)):
         (cb[i])(info, context)

   def __friendConnectionCB__(self, carrier, id, status, context):
      #print 'called friendConnectionCB handler'
      cb = self.events.friendConnection
      for i in range(0, len(cb)):
         (cb[i])(id, ConnectionState[status], context)

   def __friendInfoCB__(self, carrier, id, info, context):
      #print 'called friendInfoCB handler'
      cb = self.events.friendInfo
      if info:
         info = FriendInfo(info.contents)
      else:
         info = None
      for i in range(0, len(cb)):
         (cb[i])(id, info, context)

   def __friendPresenceCB__(self, carrier, id, presence, context):
      #print 'called friendPresenceCB handler'
      cb = self.events.friendPresence
      for i in range(0, len(cb)):
         (cb[i])(id, presence, context)

   def __friendRequestCB__(self, carrier, id, info, msg, context):
      #print 'called friendRequestCB handler'
      cb = self.events.friendRequest
      if info:
         info = UserInfo(info.contents)
      else:
         info = None      
      for i in range(0, len(cb)):
         (cb[i])(id, info, msg, context)

   def __friendAddedCB__(self, carrier, info, context):
      #print 'called friendAddedCB handler'
      cb = self.events.friendAdded
      if info:
         info = UserInfo(info.contents)
      else:
         info = None      
      for i in range(0, len(cb)):
         (cb[i])(info, context)

   def __friendRemovedCB__(self, carrier, id, context):
      #print 'called friendRemovedCB handler'
      cb = self.events.friendRemoved
      for i in range(0, len(cb)):
         (cb[i])(id, context)

   def __friendMessageCB__(self, carrier, id, msg, length, context):
      #print 'called friendMessageCB handler'
      cb = self.events.friendMessage
      for i in range(0, len(cb)):
         (cb[i])(id, msg, context) 

   def __friendInviteCB__(self, carrier, id, bundle, data, length, context):
      #print 'called friendInviteCB handler'
      cb = self.events.friendInvite
      for i in range(0, len(cb)):
         (cb[i])(id, bundle, data, context)

   def __friendsIterateCB__(self, info, context):
      #print 'called friendsIterateCB handler'
      cb = self.events.friendsIterate
      if info:
         info = FriendInfo(info.contents)      
      else:
         info = None
      for i in range(0, len(cb)):
         (cb[i])(info, context)
      return True # true says continue - maybe you're searching them?

   def __friendInviteResponseCB__(self, carrier, id, bundle, status, reason, data, length, context):
      #print 'called friendInviteResponseCB handler'
      cb = self.events.friendInviteResponse
      for i in range(0, len(cb)):
         (cb[i])(id, ConnectionState[status], reason, data, bundle, context)

   def __groupInviteCB__(self, carrier, id, cookie, length, context):
      print 'called groupInviteCB handler'
      cb = self.events.groupInvite
      for i in range(0, len(cb)):
         (cb[i])(id, cookie, context)

class CarrierSdk(Object):

   def __init__(self, libPath, opts=None, **kwargs):
      self.elaCarrier = None
      self.libCarrier = None
      self.libSession = None
      self.opts = opts
      self.callbacks = Callbacks()
      self.libPath = libPath
      self.printer = ELAPRINTLOG(self.__printer__)
      self.printerCB = None    
      for k,v in kwargs.items():
         self[k] = v

      if not libPath.endswith('/'):
        libPath += '/'
      if os.name == 'nt':
        pwd = os.curdir
        os.chdir(self.libPath)
        self.libCarrier = ctypes.CDLL('elacarrier.dll')
        #self.libSession = ctypes.CDLL('elasession.dll')
        os.chdir(pwd)
      else:
        self.libCarrier = ctypes.CDLL(libPath + 'libelacarrier.so')
        #self.libCarrier = ctypes.CDLL(libPath + 'libelasession.so')     

      __createElaCarrierInterfaces__(self.libCarrier)

   # cb for log printing - need to make this a C func with friendly cb?
   # *** something wrong with va_list ***
   def __printer__(self, fmt, args):
      if self.printerCB:
         buf = ctypes.create_string_buffer('x' * 200)
         rc = snprintf(buf, ctypes.sizeof(buf), fmt, args)
         print rc, buf.value
         if self.printerCB:
            (self.printerCB)(buf.value)

   def getVersion(self):
      return self.libCarrier.ela_get_version()

   def getInfo(self):
      o = Object()
      for prop, ctype in self.elaCarrier.contents._fields_:
         # should check for pointers
         try:
            o[prop] = getattr(self.elaCarrier.contents, prop)   
         except Exception as e:
            print e
            o[prop] = ctype
      return o
   
   def initLog(self, level, path=None, printer=None):
      self.printerCB = printer
      return self.libCarrier.ela_log_init(level, path, self.printer)

   def addrIsValid(self, addr):
      return self.libCarrier.ela_address_is_valid(addr)

   def idIsValid(self, id):
      return self.libCarrier.ela_id_is_valid(id)
   
   def getError(self):
      n = self.libCarrier.ela_get_error()
      return Error(n)
   
   def clearError(self):
      self.libCarrier.ela_clear_error()
 
   def new(self, opts, context=None):
      elaOpts = ELAOPTIONS()      
      elaOpts.persistent_location = opts.persistentLocation
      elaOpts.udp_enabled = opts.udpEnabled
      elaOpts.bootstrap_size = opts.bootstraps.len()
      elaOpts.bootstraps = opts.bootstraps.get_ela()

      elaCallbacks = self.callbacks.elaCallbacks
      elaContext = context

      self.elaCarrier = self.libCarrier.ela_new(ctypes.byref(elaOpts), ctypes.byref(elaCallbacks), elaContext)     
      return self.elaCarrier

   def run(self, interval):
      return self.libCarrier.ela_run(self.elaCarrier, interval)     

   def kill(self):
      return self.libCarrier.ela_kill(self.elaCarrier)

   def getAddress(self):
      buffer = ctypes.create_string_buffer(ELA_MAX_ADDRESS_LEN + 1)
      addr = self.libCarrier.ela_get_address(self.elaCarrier, buffer, ELA_MAX_ADDRESS_LEN + 1)
      if not addr:
         return None
      else:
         return addr

   def getNodeId(self):
      buffer = ctypes.create_string_buffer(ELA_MAX_ID_LEN + 1)
      id = self.libCarrier.ela_get_nodeid(self.elaCarrier, buffer, ELA_MAX_ID_LEN + 1)
      if not id:
         return None
      else:
         return id

   def getUserId(self):
      buffer = ctypes.create_string_buffer(ELA_MAX_ID_LEN + 1)
      id = self.libCarrier.ela_get_userid(self.elaCarrier, buffer, ELA_MAX_ID_LEN + 1)
      if not id:
         return None
      else:
         return id

   def getUserInfo(self):
      info = ELAUSERINFO()
      rc = self.libCarrier.ela_get_self_info(self.elaCarrier, ctypes.byref(info))
      if rc:
         return None
      else:
         return UserInfo(info)

   def setUserInfo(self, info):
      info = info.get_ela()
      return self.libCarrier.ela_set_self_info(self.elaCarrier, ctypes.byref(info))

   def getPresence(self):
      p = ELAPRESENCESTATUS()
      rc = self.libCarrier.ela_get_self_presence(self.elaCarrier, ctypes.byref(p))
      if rc:
         return None
      else:
         return Presence[p.value]

   def setPresence(self, presence):
      return self.libCarrier.ela_set_self_presence(self.elaCarrier, Presence[presence])     

   def getFriends(self, context=None):
      return self.libCarrier.ela_get_friends(self.elaCarrier, self.callbacks.friendsIterate, context)

   def getFriendInfo(self, id):
      info = ELAFRIENDINFO()
      rc = self.libCarrier.ela_get_friend_info(self.elaCarrier, id, ctypes.byref(info))
      if rc:
         return None
      else:
         return FriendInfo(info)      

   def addFriend(self, address, msg):
      return self.libCarrier.ela_add_friend(self.elaCarrier, address, msg)

   def labelFriend(self, id, label):
      return self.libCarrier.ela_set_friend_label(self.elaCarrier, id, label)
      
   def sendMsg(self, id, msg):
      return self.libCarrier.ela_send_friend_message(self.elaCarrier, id, msg, len(msg)+1)
   
   def acceptFriend(self, id):
      return self.libCarrier.ela_accept_friend(self.elaCarrier, id)

   def removeFriend(self, id):
      return self.libCarrier.ela_remove_friend(self.elaCarrier, id)

   def isFriend(self, id):
      return self.libCarrier.ela_is_friend(self.elaCarrier, id)

   def inviteFriend(self, id, data, bundle=None, context=None):
      return self.libCarrier.ela_invite_friend(self.elaCarrier, id, bundle, data, len(data) + 1,  self.callbacks.friendInviteResponse, context)

   def replyFriendInvite(self, id, status, reason, data, bundle=None):
     if not isinstance(status, (int, long)):
       raise ValueError('"status" must be an integer')
     return self.libCarrier.ela_reply_friend_invite(self.elaCarrier, id, bundle, status, reason, data, len(data) + 1)
