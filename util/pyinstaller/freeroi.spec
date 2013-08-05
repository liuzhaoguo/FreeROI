# -*- mode: python -*-
a = Analysis(['F:\\FreeROI\\FreeROI\\bin\\freeroi'],
             pathex=['F:\\FreeROI\\pyinstaller-2.0'],
             #hiddenimports=['scipy.signal', 'skimage.transform'],
             hiddenimports=[],
             hookspath=None)
             #hookspath='F:\FreeROI\pyinstaller-2.0\freeroi\pri_hook')
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\freeroi', 'freeroi.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               [('skimage._shared.geometry', 'C:\Python27\Lib\site-packages\skimage\_shared\geometry.pyd', 'EXTENSION')],
               [('skimage._shared.interpolation', 'C:\Python27\Lib\site-packages\skimage\_shared\interpolation.pyd', 'EXTENSION')],
               #[('skimage._shared.transform', 'C:\Python27\Lib\site-packages\skimage\_shared\transform.pyd', 'EXTENSION')],
               [('sigtools', 'C:\Python27\Lib\site-packages\scipy\signal\sigtools.pyd', 'EXTENSION')],
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'freeroi'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'freeroi.app'))
