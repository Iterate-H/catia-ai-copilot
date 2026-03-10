# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 打包配置 — 生成单文件 exe
# 用法: pip install pyinstaller && pyinstaller build.spec

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('examples', 'examples'),
    ],
    hiddenimports=[
        'PyQt5.sip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['streamlit', 'matplotlib', 'numpy', 'pandas'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CATIA宏参数化工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)
