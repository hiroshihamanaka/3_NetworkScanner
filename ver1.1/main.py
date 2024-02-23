
# main.py
import sys
from PyQt5.QtWidgets import QApplication
from NetworkScanner.Init_GUI import InitGUI
from NetworkScanner.Logging_Config import setup_logging

def main():
    # Initialize the application
    app = QApplication(sys.argv)
    setup_logging()
    ex = InitGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
