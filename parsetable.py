NAME_TABLE = 0xC9604000
FILE_TABLE = 0xC9623400
BITMAP_TABLE = 0xCB757400
DATA_START = 0xCFDB0400
BITMAP_SIZE = 0x9000

import string


class FileTable(object):
    def __init__(self, dev):
        self.dev = dev
        self.avail = {}
        self.parse()

    def parse(self):
        self.avail = {}

        with open(self.dev, 'rb') as f:
            f.seek(FILE_TABLE)
            for slot in range(0, 1999):
                data = f.read(0x4400)
                if data[:2] != "\xff\xff":
                    self.avail[slot] = data[2:41].strip("\x00")

    def __str__(self):
        r = []
        for k, v in self.avail.iteritems():
#            bt = BitmapTable(self.dev, k)
#            r.append("%d - %s (%d)" % (k, v, bt.expected_size))
            r.append("%d - %s" % (k, v))

        return "\n".join(r)


class BitmapTable(object):
    def __init__(self, dev, slot):
        self.dev = dev
        self.bmap = None
        self.slot = slot
        self.parse()

    def parse(self):
        with open(self.dev, 'rb') as f:
            f.seek(BITMAP_TABLE + (self.slot + 1) * BITMAP_SIZE)
            rawbmap = f.read(BITMAP_SIZE)
            self.bmap = "".join([string.zfill(bin(ord(c))[2:], 8) for c in rawbmap])

    def dumpfile(self, outfn):
        with open(self.dev, 'rb') as f, open(outfn, 'w+b') as fout:
            fout.write("\x00" * 2648)
            bidx = 0
            for b in self.bmap:
                if b == '1':
                    f.seek(DATA_START + (bidx * 512 * 1040))
                    fout.write(f.read(512 * 1040))

                bidx += 1

    @property
    def expected_size(self):
        bcnt = 0
        for b in self.bmap:
            if b == '1':
                bcnt += 1

        return bcnt * 512 * 1040
