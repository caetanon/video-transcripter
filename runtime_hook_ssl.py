import os
import sys

# Fix SSL certificates for PyInstaller bundles on Windows
if hasattr(sys, '_MEIPASS'):
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    except ImportError:
        pass
