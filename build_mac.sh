#!/bin/bash
set -e

echo "==> Ativando venv..."
source venv/bin/activate

echo "==> Limpando builds anteriores..."
rm -rf build dist

echo "==> Gerando .app com PyInstaller..."
pyinstaller build.spec

echo ""
echo "✓ Build concluido!"
echo "  App: dist/VideoTranscriber.app"
echo ""
echo "Para criar o .dmg (opcional):"
echo "  brew install create-dmg"
echo "  create-dmg --volname 'Video Transcriber' --app-drop-link 600 185 dist/VideoTranscriber.dmg dist/VideoTranscriber.app"
