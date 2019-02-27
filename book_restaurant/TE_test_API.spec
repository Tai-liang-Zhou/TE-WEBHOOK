# -*- mode: python -*-

block_cipher = None


a = Analysis(['TE_test_API.py'],
             pathex=['C:\\Users\\Tom\\Documents\\¦Ë¶¡´¼¯à\\te-webhook.tar\\te-webhookv2\\te-webhook\\book_restaurant'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          name='TE_test_API',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
