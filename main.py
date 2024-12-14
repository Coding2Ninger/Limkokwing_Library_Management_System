import sys
from PyQt5.QtWidgets import QApplication
from library_app import LibraryApp

def main():
    app = QApplication(sys.argv)
    library_app = LibraryApp()
    library_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
