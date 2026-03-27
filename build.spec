import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files

block_cipher = None

# Collect customtkinter, whisper and torch assets (torch inclui DLLs do CUDA)
ctk_datas, ctk_binaries, ctk_hiddenimports = collect_all('customtkinter')
whisper_datas, whisper_binaries, whisper_hiddenimports = collect_all('whisper')
torch_datas, torch_binaries, torch_hiddenimports = collect_all('torch')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=ctk_binaries + whisper_binaries + torch_binaries,
    datas=ctk_datas + whisper_datas + torch_datas + [('ui', 'ui')],
    hiddenimports=ctk_hiddenimports + whisper_hiddenimports + torch_hiddenimports + [
        'tiktoken',
        'tiktoken_ext',
        'tiktoken_ext.openai_public',
        'torch',
        'torch.cuda',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VideoTranscriber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='VideoTranscriber',
)

# Mac .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='VideoTranscriber.app',
        icon=None,
        bundle_identifier='com.cnlabs.videotranscriber',
        info_plist={
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '12.0',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHumanReadableCopyright': 'CNLabs',
        },
    )
