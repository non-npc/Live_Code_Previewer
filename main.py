import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QSplitter, QCheckBox,
    QMenuBar, QAction, QMessageBox, QMainWindow
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings, QWebEngineProfile, QWebEngineView
from PyQt5.QtCore import QUrl, Qt
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Menu bar setup
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu('File')

        # Quit action
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.quit_app)
        file_menu.addAction(quit_action)

        # Help menu
        help_menu = menu_bar.addMenu('Help')

        # About action under Help menu
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Splitter to divide the columns equally
        splitter = QSplitter(Qt.Horizontal)

        # Left column with label, text area, button, and toggle
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.label = QLabel('Enter HTML/CSS/JS content:')
        self.text_area = QTextEdit()
        self.text_area.textChanged.connect(self.on_text_change)  # Connect text change signal

        self.load_button = QPushButton('Load in Webview')
        self.load_button.clicked.connect(self.load_html)

        # Checkbox for toggling live updating
        self.live_update_checkbox = QCheckBox('Toggle Live Updating')
        self.live_update_checkbox.stateChanged.connect(self.toggle_live_update)

        # Checkbox for toggling debug mode
        self.debug_checkbox = QCheckBox('Toggle Debug Console')
        self.debug_checkbox.stateChanged.connect(self.toggle_debug)

        left_layout.addWidget(self.label)
        left_layout.addWidget(self.text_area)
        left_layout.addWidget(self.load_button)
        left_layout.addWidget(self.live_update_checkbox)
        left_layout.addWidget(self.debug_checkbox)

        # Right column with WebView and label
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.webview_label = QLabel('Webview:')
        self.webview = QWebEngineView()

        # Set default HTML content with grey border on body
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
        # Load default HTML with border immediately on app start
        self.webview.setHtml(self.default_html)

        # Add label and webview to right layout
        right_layout.addWidget(self.webview_label)
        right_layout.addWidget(self.webview)

        # Ensure alignment of the labels and text areas
        left_layout.setStretch(1, 1)  # Stretch the text area to fill available space
        right_layout.setStretch(1, 1)  # Stretch the webview to fill available space

        # Add the left and right columns to the splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        # Set the splitter's initial sizes to make both columns equal
        splitter.setSizes([640, 640])

        # Add the splitter to the main layout
        layout.addWidget(splitter)

        # Create a separate webview for developer tools
        self.dev_tools = QWebEngineView()

        self.setWindowTitle('Live Code Previewer')
        self.resize(1280, 720)

    def load_html(self):
        # Get body content from the text area
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

        # Load the new HTML into the webview
        self.webview.setHtml(html_with_body, QUrl.fromLocalFile(os.getcwd() + '/'))

    def toggle_live_update(self, state):
        # Check if the checkbox is checked (live updating enabled)
        if state == Qt.Checked:
            # Disable the load button when live updating is enabled
            self.load_button.setEnabled(False)
        else:
            # Enable the load button when live updating is disabled
            self.load_button.setEnabled(True)

    def toggle_debug(self, state):
        # Toggle the webview developer tools (debug mode)
        if state == Qt.Checked:
            # Open the dev tools in a separate window
            self.webview.page().setDevToolsPage(self.dev_tools.page())
            self.dev_tools.show()
        else:
            # Close the dev tools window when debug is turned off
            self.dev_tools.hide()

    def on_text_change(self):
        # If live updating is enabled, automatically update the webview
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
