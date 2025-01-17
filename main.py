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

        # include channel
        self.include_channel = QPushButton("Include Channel")
        self.include_channel.setCheckable(True)
        self.include_channel.clicked.connect(self.update_preview)

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
        self.message_link_layout = QHBoxLayout()
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
        self.input_layout.addWidget(self.include_channel)
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
        first_line = self.build_first_line(
            author=self.author.text(),
            author_id=self.author_id.text(),
            message_link=self.message_link.text(),
            reply_ping=self.reply_ping.isChecked(),
            include_channel=self.include_channel.isChecked()
        )

        self.preview.setPlainText(f"-# > {first_line}\n"
                                  f"{self.process_reply_text(self.reply_text.toPlainText())}"
                                  f"\n"
                                  f"{self.message_text.toPlainText()}")

    @staticmethod
    def build_first_line(author: str, author_id: str, message_link: str, reply_ping: bool, include_channel: bool):
        first_line = str

        if author or (author_id and reply_ping):
            if reply_ping and author_id:
                first_line = f"<@{author_id}>"

            else:
                first_line = author

            if message_link and include_channel:
                first_line = f"{author} in <#{message_link.split('/')[-2]}>"

            if message_link:
                first_line = f"[Reply to:](<{message_link}>) {first_line}"
            else:
                first_line = f"Reply to: {first_line}"

        return first_line

    @staticmethod
    def process_reply_text(text):

        if len(text) > 37:
            text = f"{text[:37]}..."

        lines = []
        for i, line in enumerate(text.splitlines()):
            if i < 3:
                if i == 2 and i < len(text.splitlines()) - 1:
                    lines.append(f"> {line}...\n")
                else:
                    lines.append(f"> {line}\n")

        text = str.join('', lines)

        return text

    def copy_handler(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.preview.toPlainText())

        self.copy.setText("Copied to clipboard!")
        QTimer.singleShot(2000, lambda: self.copy.setText("Copy"))

    def create_line_edit(self, placeholder):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setMinimumWidth(150)
        line_edit.textChanged.connect(self.update_preview)
        return line_edit

    def create_text_edit(self, placeholder):
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
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
