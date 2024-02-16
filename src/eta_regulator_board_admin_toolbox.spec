# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['bootstrapper.py'],
    pathex=['../.venv/Lib/site-packages'],
    binaries=[],
    datas=[('assets/favicon.ico', 'src/assets'), ('assets/icon.png', 'src/assets')],
    hiddenimports=['main.py'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='eta_regulator_board_admin_toolbox',
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
    icon=['assets\\favicon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='eta_regulator_board_admin_toolbox',
)
