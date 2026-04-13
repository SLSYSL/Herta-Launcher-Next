# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import shutil
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('./assets', './assets'),
        ('./tui/style.tcss', './tui')
    ],
    hiddenimports=collect_submodules('textual.widget') + collect_submodules('textual.widgets'),
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
    a.binaries,
    a.datas,
    [],
    name='Herta-Launcher-Next',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

if os.path.exists("build"): shutil.rmtree("build")
