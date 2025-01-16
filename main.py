from PySide6.QtCore import *
from PySide6.QtWidgets import *


class ReplyGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # set up the window
        self.setWindowTitle("Reply Generator")

        # author details
        self.author = self.create_line_edit("Reply Author:")
        self.author_id = self.create_line_edit("Reply Author ID:")

        # reply ping button
        self.reply_ping = QPushButton("Reply\nPing")
        self.reply_ping.clicked.connect(self.update_preview)
        self.reply_ping.setCheckable(True)
        self.reply_ping.setMaximumSize(100, 100)

        # message link
        self.message_link = self.create_line_edit("Link to replied message:")

        # replied message text
        self.reply_text = self.create_text_edit("Replied text:")

        # message text
        self.message_text = self.create_text_edit("Your reply:")

        # preview
        self.preview = QTextBrowser()
        self.copy = QPushButton("Copy")
        self.copy.pressed.connect(self.copy_handler)

        # layouts
        self.main_layout = QHBoxLayout()
        self.preview_layout = QVBoxLayout()
        self.input_layout = QVBoxLayout()
        self.author_layout = QHBoxLayout()
        self.author_info_layout = QVBoxLayout()

        # set size and alignment
        self.author_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.author_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        # fill author info layout
        self.author_info_layout.addWidget(self.author)
        self.author_info_layout.addWidget(self.author_id)

        # fill author layout
        self.author_layout.addLayout(self.author_info_layout)
        self.author_layout.addWidget(self.reply_ping)

        # fill input layout
        self.input_layout.addLayout(self.author_layout)
        self.input_layout.addWidget(self.message_link)
        self.input_layout.addWidget(self.reply_text)
        self.input_layout.addWidget(self.message_text)

        # fill preview layout
        self.preview_layout.addWidget(self.preview)
        self.preview_layout.addWidget(self.copy)

        # fill main layout
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.preview_layout)

        # set main layout
        self.setLayout(self.main_layout)

    def update_preview(self):
        author = ''
        link_components = self.message_text.text().split('/')

        if self.author.text() or self.author_id.text():
            if self.reply_ping.isChecked() and self.author_id.text():
                author = f"<@{self.author_id.text()}>"
            else:
                author = f"{self.author.text}"

            if self.message_link.text():
                author = f"{self.author.text} in <#{link_components[5]}>"

        if self.message_link.text():
            reply_to_text = f"[Reply to:](<{self.message_link.text()}>)"
        else:
            reply_to_text = "Reply to:"

        self.preview.setPlainText(f"-# > {reply_to_text} {author}\n"
                                  f"> {self.reply_text.text()}\n"
                                  f"_ _\n"
                                  f"{self.message_text.text()}")

    def copy_handler(self):
        clipboard = QApplication.clipboard()
        clipboard.setText("temp")

        self.copy.setText("Copied to clipboard!")
        QTimer.singleShot(2000, lambda: self.copy.setText("Copy"))

    def create_line_edit(self, placeholder):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setMinimumWidth(150)
        line_edit.textChanged.connect(self.update_preview)
        return line_edit

    def create_text_edit(self, placeholder):
        text_edit = QLineEdit()
        text_edit.setPlaceholderText(placeholder)
        text_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        text_edit.textChanged.connect(self.update_preview)
        return text_edit


def main():
    app = QApplication([])
    window = ReplyGenerator()  # Create an instance of MyWindow
    window.update_preview()
    window.show()  # Show the window
    app.exec()  # Start the application's event loop


if __name__ == "__main__":
    main()
