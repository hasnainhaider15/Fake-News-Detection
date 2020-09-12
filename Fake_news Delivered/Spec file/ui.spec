# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['ui.py'],
             pathex=['C:\\Users\\SUNNY\\Desktop\\Fake_news Delivered'],
             binaries=[],
             datas=[('c:/Users/SUNNY/Desktop/Fake_news Delivered/login.ui', '.' ), ('c:/Users/SUNNY/Desktop/Fake_news Delivered/register.ui', '.' ),('c:/Users/SUNNY/Desktop/Fake_news Delivered/reset.ui', '.' ), ('c:/Users/SUNNY/Desktop/Fake_news Delivered/chose.ui', '.' ),('c:/Users/SUNNY/Desktop/Fake_news Delivered/ocr.ui', '.' ),('c:/Users/SUNNY/Desktop/Fake_news Delivered/textdetect.ui', '.' ),('c:/Users/SUNNY/Desktop/Fake_news Delivered/firebasedatabase.py', '.' ),('c:/Users/SUNNY/Desktop/Fake_news Delivered/datashow.py', '.' ),('c:/Users/SUNNY/Desktop/Fake_news Delivered/newdata.csv', '.')],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=['c://Users//SUNNY/Desktop/Fake_news Delivered/hook-gcloud.py'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
