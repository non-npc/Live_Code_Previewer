import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QSplitter, QCheckBox,
    QMenuBar, QAction, QMessageBox, QMainWindow
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')

        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.quit_app)
        file_menu.addAction(quit_action)

        help_menu = menu_bar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.label = QLabel('Enter HTML/CSS/JS content:')
        self.text_area = QTextEdit()
        self.text_area.textChanged.connect(self.on_text_change)

        self.load_button = QPushButton('Load in Webview')
        self.load_button.clicked.connect(self.load_html)

        self.live_update_checkbox = QCheckBox('Toggle Live Updating')
        self.live_update_checkbox.stateChanged.connect(self.toggle_live_update)

        self.debug_checkbox = QCheckBox('Toggle Debug Console')
        self.debug_checkbox.stateChanged.connect(self.toggle_debug)

        left_layout.addWidget(self.label)
        left_layout.addWidget(self.text_area)
        left_layout.addWidget(self.load_button)
        left_layout.addWidget(self.live_update_checkbox)
        left_layout.addWidget(self.debug_checkbox)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.webview_label = QLabel('Webview:')
        self.webview = QWebEngineView()

        self.default_html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Webview Content</title>
            <style>
                body {{
                    margin: 0;
                    padding: 10px;
                    border: 1px solid grey;
                    height: 100vh;
                    box-sizing: border-box;
                }}
            </style>
        </head>
        <body>
            <!-- Body content will be injected here -->
        </body>
        </html>
        '''
        self.webview.setHtml(self.default_html)

        right_layout.addWidget(self.webview_label)
        right_layout.addWidget(self.webview)

        left_layout.setStretch(1, 1)
        right_layout.setStretch(1, 1)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([640, 640])

        layout.addWidget(splitter)

        self.dev_tools = None

        self.setWindowTitle('Live Code Previewer')
        self.resize(1280, 720)

    def load_html(self):
        body_content = self.text_area.toPlainText()

        # Inject body content into the base HTML and keep the grey border
        html_with_body = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Webview Content</title>
            <style>
                body {{
                    margin: 0;
                    padding: 10px;
                    border: 1px solid grey;
                    height: 100vh;
                    box-sizing: border-box;
                }}
            </style>
        </head>
        <body>
            {}
        </body>
        </html>
        '''.format(body_content)

        self.webview.setHtml(html_with_body, QUrl.fromLocalFile(os.getcwd() + '/'))

    def toggle_live_update(self, state):
        if state == Qt.Checked:
            self.load_button.setEnabled(False)
        else:
            self.load_button.setEnabled(True)

    def toggle_debug(self, state):
        if state == Qt.Checked:
            if self.dev_tools is None or not self.dev_tools.isVisible():
                self.dev_tools = QWebEngineView()
                self.webview.page().setDevToolsPage(self.dev_tools.page())
                
                self.dev_tools.closeEvent = self.cleanup_devtools

                self.dev_tools.show()
        else:
            if self.dev_tools is not None:
                self.webview.page().setDevToolsPage(None)
                self.dev_tools.close()
                self.dev_tools = None

    def cleanup_devtools(self, event):
        self.webview.page().setDevToolsPage(None)
        self.dev_tools = None
        self.debug_checkbox.setChecked(False)
        event.accept()

    def on_text_change(self):
        if self.live_update_checkbox.isChecked():
            self.load_html()

    def quit_app(self):
        QApplication.quit()

    def show_about(self):
        QMessageBox.about(self, "About", "Live Code Previewer\nVersion 1.0\nCreated by non-npc Sep/12/2024")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
