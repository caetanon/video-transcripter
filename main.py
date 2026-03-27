import sys
import os

# Fix para PyInstaller no Windows: stdout/stderr são None em modo windowed
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

from ui.app import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
