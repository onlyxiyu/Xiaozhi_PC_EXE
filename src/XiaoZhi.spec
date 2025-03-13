# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('../vosk-model-cn-kaldi-multicn-0.15', 'vosk-model-cn-kaldi-multicn-0.15'), ('C:\\Users\\xiyu\\PycharmProjects\\PythonProject2\\.venv\\Lib\\site-packages\\vosk', 'vosk')]
binaries = [('../config.json', '.'), ('C:\\Users\\xiyu\\PycharmProjects\\PythonProject2\\.venv\\Lib\\site-packages\\vosk\\libgcc_s_seh-1.dll', '.'), ('C:\\Users\\xiyu\\PycharmProjects\\PythonProject2\\.venv\\Lib\\site-packages\\vosk\\libstdc++-6.dll', '.'), ('C:\\Users\\xiyu\\PycharmProjects\\PythonProject2\\.venv\\Lib\\site-packages\\vosk\\libvosk.dll', '.'), ('C:\\Users\\xiyu\\PycharmProjects\\PythonProject2\\.venv\\Lib\\site-packages\\vosk\\libwinpthread-1.dll', '.')]
hiddenimports = ['edge_tts', 'vosk', 'sounddevice', 'numpy', 'pygame']
tmp_ret = collect_all('vosk')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='XiaoZhi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='XiaoZhi',
)
