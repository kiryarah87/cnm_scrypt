# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('data/*.xlsx', 'data'),
    ],
    hiddenimports=[
        'python_calamine',
        'openpyxl',
        'pandas',
        'xlsxwriter',
    ],
    hookspath=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='cnm_scrypt',
    debug=False,
    strip=False,
    upx=True,
    console=True,
    onefile=True,
)
