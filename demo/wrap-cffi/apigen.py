import sys, os.path as p
wdir = p.abspath(p.dirname(__file__))
topdir = p.normpath(p.join(wdir, p.pardir, p.pardir))
srcdir = p.join(topdir, 'src')
sys.path.insert(0, p.join(topdir, 'conf'))

from mpiscanner import Scanner
scanner = Scanner()
libmpi_pxd = p.join(srcdir, 'include', 'mpi4py', 'libmpi.pxd')
scanner.parse_file(libmpi_pxd)
libmpi_h = p.join(wdir, 'libmpi.h')
scanner.dump_header_h(libmpi_h)

#try:
#    from cStringIO import StringIO
#except ImportError:
#    from io import StringIO
#libmpi_h = StringIO()
#scanner.dump_header_h(libmpi_h)
#print libmpi_h.read()

libmpi_c = p.join(wdir, 'libmpi.c')
f = open(libmpi_c, 'w')
f.write(
"""\
#include <mpi.h>
#include "%(srcdir)s/config.h"
#include "%(srcdir)s/missing.h"
#include "%(srcdir)s/fallback.h"
#include "%(srcdir)s/compat.h"
""" % vars()
)
f.close()
