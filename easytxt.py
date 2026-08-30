import os
import sys
import ctypes

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import uic


def resource_path(filename):
    """Encontra arquivos do PyTXT no Python e no EXE."""

    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)

        paths = [
            os.path.join(base_dir, filename),
            os.path.join(base_dir, "_internal", filename)
        ]

    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        paths = [
            os.path.join(base_dir, filename)
        ]

    for path in paths:
        if os.path.isfile(path):
            return path

    raise FileNotFoundError(
        f"Arquivo não encontrado: {filename}\n\n"
        f"Caminhos procurados:\n" +
        "\n".join(paths)
    )


class FontDialog(QDialog):

    def __init__(self, current_font, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Font Info")

        layout = QVBoxLayout(self)

        font_label = QLabel("Font:")

        self.font_box = QFontComboBox()
        self.font_box.setCurrentFont(current_font)

        size_label = QLabel("Size:")

        self.size_box = QSpinBox()
        self.size_box.setRange(1, 100)
        self.size_box.setValue(current_font.pointSize())

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(font_label)
        layout.addWidget(self.font_box)
        layout.addWidget(size_label)
        layout.addWidget(self.size_box)
        layout.addWidget(buttons)

    def get_font(self):
        font = QFont(self.font_box.currentFont())
        font.setPointSize(self.size_box.value())
        return font


class TheGUI(QMainWindow):

    def __init__(self):
        super(TheGUI, self).__init__()

        ui_path = resource_path("untitled.ui")

        uic.loadUi(ui_path, self)

        self.setWindowTitle("PyTXT")

        icon_path = resource_path("PyTXT.ico")

        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.actionOpen.triggered.connect(
            self.open_file
        )

        self.actionSave.triggered.connect(
            self.save_file
        )

        self.actionExit.triggered.connect(
            self.close
        )

        self.actionUndo.triggered.connect(
            self.textEdit.undo
        )

        self.actionRedo.triggered.connect(
            self.textEdit.redo
        )

        self.actionCopy.triggered.connect(
            self.textEdit.copy
        )

        self.actionSelect_All.triggered.connect(
            self.textEdit.selectAll
        )

        self.actionLight_Mode.triggered.connect(
            self.light_mode
        )

        self.actionDark_Mode.triggered.connect(
            self.dark_mode
        )

        self.actionEdit_Font_Info.triggered.connect(
            self.edit_font
        )

        self.show()


    def open_file(self):

        options = QFileDialog.Options()

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if filename:

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as f:

                self.textEdit.setText(
                    f.read()
                )

    def save_file(self):

        options = QFileDialog.Options()

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if filename:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    self.textEdit.toPlainText()
                )

    def light_mode(self):

        self.setStyleSheet("")

    def dark_mode(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #202020;
            }

            QTextEdit {
                background-color: #181818;
                color: #eeeeee;
                border: 1px solid #444444;
                selection-background-color: #555555;
            }

            QMenuBar {
                background-color: #202020;
                color: #eeeeee;
            }

            QMenuBar::item:selected {
                background-color: #404040;
            }

            QMenu {
                background-color: #202020;
                color: #eeeeee;
            }

            QMenu::item:selected {
                background-color: #404040;
            }

            QStatusBar {
                background-color: #202020;
                color: #eeeeee;
            }
        """)

    def edit_font(self):

        dialog = FontDialog(
            self.textEdit.font(),
            self
        )

        if dialog.exec_() == QDialog.Accepted:

            self.textEdit.setFont(
                dialog.get_font()
            )


def main():

    try:

        myappid = "mycompany.easytxt.editor.1.0"

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            myappid
        )

    except Exception:
        pass

    app = QApplication(sys.argv)

    window = TheGUI()

    sys.exit(
        app.exec_()
    )


if __name__ == "__main__":
    main()
