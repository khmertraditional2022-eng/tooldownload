import sys
import os
import ctypes

# Suppress annoying Qt font warnings on Windows
os.environ['QT_LOGGING_RULES'] = 'qt.qpa.fonts.warning=false'

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from gui.main_window import MainWindow
from core.updater import check_for_updates

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    # Tell Windows to use the app's icon on the taskbar instead of Python's default icon
    try:
        myappid = 'mycompany.reeldownloader.1.0' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass
        
    app = QApplication(sys.argv)
    
    # Load custom fonts using resource path
    font_dir = get_resource_path('fonts')
    if os.path.exists(font_dir):
        QFontDatabase.addApplicationFont(os.path.join(font_dir, 'Battambang-Regular.ttf'))
        QFontDatabase.addApplicationFont(os.path.join(font_dir, 'Battambang-Bold.ttf'))
        
    app.setFont(QFont("Battambang", 10))
    
    window = MainWindow()
    
    # Check for updates (will show a dialog if update is available)
    check_for_updates(window)
    
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
