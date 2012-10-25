import blkreader, time

#btcdir='' # change this to the folder where blk0001.dat is located

blk0001=blkreader.blkfile(btcdir+'/blk0001.dat')

genesisblock=blk0001.getblock()

print
print 'GENESIS BLOCK'
print ' magic value:   ', genesisblock.magic.encode('hex')
print ' version:       ', genesisblock.version
print ' size:          ', genesisblock.size,'bytes'
print ' hash:          ', genesisblock.hash
print ' previous block:', genesisblock.prevblock
print ' merkle root:   ', genesisblock.merkleroot
print ' timestamp:     ', time.asctime(genesisblock.timestamp)
print ' bits:          ', genesisblock.bits.encode('hex')
print ' nonce:         ', genesisblock.nonce
#print ' header:        ', genesisblock.header.encode('hex')
print ' number of transactions:', genesisblock.txcount
for tx in genesisblock.tx:
 print '  tx', genesisblock.tx.index(tx)
 print '   version:', tx.version
 print '   size:   ', tx.size
 print '   hash:   ', tx.hash
 print '   number of inputs:', tx.numinputs
 for txin in tx.inputs:
  print '    input', tx.inputs.index(txin)
  print '    previous output:', txin.prevouthash
  print '    n:', txin.prevoutn
  if txin.prevouthash=='0'*64: print '    coinbase:', txin.coinbase.__repr__()
  else: print '    scriptSig:', txin.script.encode('hex')
  print '    sequence:', txin.sequence
 print '   number of outputs:', tx.numoutputs
 for txout in tx.outputs:
  print '    output', tx.outputs.index(txout)
  print '    value:', txout.value
  print '    script:', txout.script.encode('hex')
 print '   lock time:', tx.locktime
  

#print ' raw block:     ', genesisblock.raw.encode('hex')
print
print 'position @ blk0001.dat:', blk0001.tell()
print
#print '2nd block, raw:',blk0001.readblock().encode('hex')