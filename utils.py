#!/usr/bin/python

# accessible by [] and .
class Object(dict):

   def __init__(self, *args, **kwargs):
      self.update(*args, **kwargs)

   def __getattr__(self, p):
      return self.get(p)

   def __setattr__(self, p, v):
      self.__setitem__(p, v)

   def __setitem__(self, p, v):
      super(Object, self).__setitem__(p, v)
      self.__dict__.update({p: v})

   def __missing__(self, p):
      v = self[p] = type(self)()

   # __delattr__
   # __delitem__
   # __getstate__
   # __setstate__

# bidi enum
class Enum(Object):
   def __init__(self, **kwargs):
      for k,v in kwargs.items():
         self[k] = v
         self[str(v)] = k
         self[int(v)] = k

   def __getattr__(self, p):
      if self.has_key(p):
         return self.get(p)
      else:
         raise LookupError

   def __getitem__(self, p):
      if self.__dict__.has_key(p):
         return self.__dict__[p]
      else:
         raise LookupError