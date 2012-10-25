# Python 2.5

import time, hashlib

def hash256(x): return hashlib.sha256(hashlib.sha256(x).digest()).digest()

class fstring():    # file methods for strings

 def __init__(self, somestring):
  self.pos=0
  self.string=somestring
 
 def read(self, length=None):
  if length==None: length=len(self.string)
  out=self.string[self.pos:self.pos+length]; self.pos+=length
  return out
 
 def seek(self, point): self.pos=point
 
 def tell(self): return self.pos

class txinput():

 def __init__(self, handle):
 
  if type(handle)==str: handle=fstring(handle)
  startingpos = handle.tell()
  
  self.prevouthash = handle.read(32)[::-1].encode('hex')
  self.prevoutn = sum([ord(handle.read(1))*(256**x) for x in range(4)])
  
  if self.prevouthash=='0'*64:
   self.coinbasesize = ord(handle.read(1))
   if self.coinbasesize>=253: self.coinbasesize = sum([ord(handle.read(1))*(256**x) for x in range(2*(self.coinbasesize-252))])
   self.coinbase = handle.read(self.coinbasesize)
   self.sequence = sum([ord(handle.read(1))*(256**x) for x in range(4)])
  
  else:
   self.scriptsize = ord(handle.read(1))
   if self.scriptsize>=253: self.scriptsize = sum([ord(handle.read(1))*(256**x) for x in range(2*(self.scriptsize-252))])
   self.script = handle.read(self.scriptsize)
   self.sequence = sum([ord(handle.read(1))*(256**x) for x in range(4)])

class txoutput():

 def __init__(self, handle):
 
  if type(handle)==str: handle=fstring(handle)
  startingpos = handle.tell()
  
  self.value = sum([ord(handle.read(1))*(256**x) for x in range(8)])
  self.scriptsize = ord(handle.read(1))
  if self.scriptsize>=253: self.scriptsize = sum([ord(handle.read(1))*(256**x) for x in range(2*(self.scriptsize-252))])
  self.script = handle.read(self.scriptsize)
  #self.asm

class transaction():

 def __init__(self, handle):
 
  if type(handle)==str: handle=fstring(handle)
  startingpos = handle.tell()
  
  self.version = sum([ord(handle.read(1))*(256**x) for x in range(4)])
  self.numinputs = ord(handle.read(1))
  if self.numinputs>=253: self.numinputs = sum([ord(handle.read(1))*(256**x) for x in range(2*(self.numinputs-252))])
  self.inputs = [txinput(handle) for inputnum in range(self.numinputs)]
  self.numoutputs = ord(handle.read(1))
  if self.numoutputs>=253: self.numoutputs = sum([ord(handle.read(1))*(256**x) for x in range(2*(self.numoutputs-252))])
  self.outputs = [txoutput(handle) for outputnum in range(self.numoutputs)]
  self.locktime = sum([ord(handle.read(1))*(256**x) for x in range(4)])
  self.size = handle.tell() - startingpos; handle.seek(startingpos)
  self.raw = handle.read(self.size)
  self.hash = hash256(self.raw)[::-1].encode('hex')
  
class block():

 def __init__(self, handle):
 
  if type(handle)==str: handle=fstring(handle)  
  self.magic  = handle.read(4)
  self.size   = sum([ord(handle.read(1))*(256**x) for x in range(4)])  # not used right now
  startingpos = handle.tell()
  
  self.version    =  sum([ord(handle.read(1))*(256**x) for x in range(4)])
  self.prevblock  =  handle.read(32)[::-1].encode('hex')
  self.merkleroot =  handle.read(32)[::-1].encode('hex')
  self.timestamp  =  time.gmtime(sum([ord(handle.read(1))*(256**x) for x in range(4)]))
  self.bits       =  handle.read(4)
  self.nonce      =  sum([ord(handle.read(1))*(256**x) for x in range(4)])
  
  handle.seek(startingpos)
  self.header     =  handle.read(80)
  self.hash       =  hash256(self.header)[::-1].encode('hex')
  
  self.txcount = ord(handle.read(1))
  if self.txcount>=253: self.txcount = sum([ord(handle.read(1))*(256**x) for x in range(2*(self.txcount-252))])
  self.tx = [transaction(handle) for txn in range(self.txcount)]
  self.size = handle.tell() - startingpos; handle.seek(startingpos)
  self.raw = handle.read(self.size)
  #self.merkletree
  #self.isvalid() to verify merkle tree, hash, and difficulty

class blkfile():
 def __init__(self, filename): self.file=file(filename,'rb+')
 def tell(self): return self.file.tell()
 def getblock(self): return block(self.file)
 def readblock(self): return block(self.file).raw