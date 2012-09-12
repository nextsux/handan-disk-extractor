#!/bin/env python

import sys

from parsetable import FileTable, BitmapTable

def usage():
	print "Usage: %s filename|device" % sys.argv[0]
	sys.exit(1)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()

	dev = sys.argv[1]

	ft = FileTable(dev)

	if len(sys.argv) < 3:
		print ft
		sys.exit(0)

	slot = int(sys.argv[2])
	outfn = "%d.hav" % slot
	print "Decoding video for slot %d to %s" % (slot, outfn)

	if ft.avail.has_key(slot):
		bt = BitmapTable(dev, slot)

		bt.dumpfile(outfn)
		print "Done"
		sys.exit(0)
	else:
		print "Key slot %d is empty!" % slot
		sys.exit(2)
