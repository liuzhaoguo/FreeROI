# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Setup script

"""
from distutils.core import setup, Extension

import sys, os.path, numpy
import sipdistutils

import PyQt4.pyqtconfig

config = PyQt4.pyqtconfig.Configuration()

#-- PyQt4 library configuration

# Replace the following with
#  qt_inc_dir = "path/to/Qt/include"
#  qt_lib_dir = "path/to/Qt/lib"
# when automatically extracted paths don't fit your installation.
# (Note that you should use a compatible compiler and Qt version
# as was used for building PyQt.)
qt_inc_dir = config.qt_inc_dir
qt_lib_dir = config.qt_lib_dir

#--

qt_lib_dirs = [qt_lib_dir]
qt_libraries = ['QtCore', 'QtGui']

if 'mingw32' in sys.argv:
    # Need better criterion - this should only apply to mingw32
    qt_lib_dirs.extend((qt_lib_dir.replace(r'\lib', r'\bin'),
                        os.path.dirname(PyQt4.__file__)))
    qt_libraries = [lib + '4' for lib in qt_libraries]

qimageview = Extension('pybp.gui.utilities.qimageview',
                       sources = [r'third_part/qimageview.sip'],
                       include_dirs = [numpy.get_include(),
                                       qt_inc_dir,
                                       os.path.join(qt_inc_dir, 'QtCore'),
                                       os.path.join(qt_inc_dir, 'QtGui')])
if sys.platform == 'darwin':
    # Qt is distributed as 'framwork' on OS X
    for lib in qt_libraries:
        qimageview.extra_link_args.extend(['-framework', lib])
    for d in qt_lib_dirs:
        qimageview.extra_link_args.append('-F' + d)
else:
    qimageview.libraries.extend(qt_libraries)
    qimageview.library_dirs.extend(qt_lib_dirs)

class build_ext(sipdistutils.build_ext):
    def _sip_compile(self, sip_bin, source, sbf):
        import PyQt4.pyqtconfig
        config = PyQt4.pyqtconfig.Configuration()
        self.spawn([sip_bin, '-c', self.build_temp, '-b', sbf] +
                   config.pyqt_sip_flags.split() + 
                   ['-I', config.pyqt_sip_dir, source])

for line in file('pybp/version.py'):
    if line.startswith('__version__'):
        exec line

setup(name = 'pybp',
      version = __version__,
      description = 'Brain parcellation toolbox',
      author = 'Neuroimageing Team@LiuLab',
      author_email = 'huanglijie.seal@gmail.com',
      url = '',
      download_url = '',
      packages = ['pybp',
                  'pybp.gui',
                  'pybp.gui.base',
                  'pybp.algorithm',
                  'pybp.cluster',
                  'pybp.bpio'],
      ext_modules = [qimageview],
      cmdclass = {'build_ext': build_ext})
