from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

app = QApplication([])

window = QMainWindow()
window.setWindowTitle("Reply Creator")

main_widget = QWidget()
main_layout = QHBoxLayout()


def update_markdown():
    author = author_field.text()
    author_id = author_id_field.text()
    reply_ping = ping_button.isChecked()
    replied_message_text = replied_message_text_field.toPlainText()
    replied_message_link = message_link_field.text()
    message_link_list = replied_message_link.split('/')
    message_text = message_text_field.toPlainText()

    if author or reply_ping:
        if reply_ping:
            author = f"<@{author_id}>"
        else:
            author = f"{author}"

        if replied_message_link:
            author = f"{author} in <#{message_link_list[5]}>"

    if replied_message_link:
        reply_to_text = f"[Reply to:](<{replied_message_link}>)"
    else:
        reply_to_text = "Reply to:"

    reply_text = (f"-# > {reply_to_text} {author}\n"
                  f"> {replied_message_text}\n"
                  f"_ _\n"
                  f"{message_text}")

    preview_text_browser.setPlainText(reply_text)


def copy_to_clipboard():
    clipboard = QApplication.clipboard()
    clipboard.setText(preview_text_browser.toPlainText())


# region Message Info

# region Replied Message Info

replied_message_info_layout = QVBoxLayout()

# region Author Info

author_layout = QHBoxLayout()

author_info_layout = QVBoxLayout()
author_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

author_field = QLineEdit()
author_field.setPlaceholderText("Author:")
author_field.textEdited.connect(update_markdown)

author_id_field = QLineEdit()
author_id_field.setPlaceholderText("Author ID:")
author_id_field.textEdited.connect(update_markdown)

author_info_layout.addWidget(author_field)
author_info_layout.addWidget(author_id_field)

author_layout.addLayout(author_info_layout)

ping_button = QPushButton("Reply\nPing")
ping_button.setCheckable(True)
ping_button.setMaximumSize(48, 48)
ping_button.setMinimumSize(48, 48)
ping_button.toggled.connect(update_markdown)

author_layout.addWidget(ping_button)
author_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

replied_message_info_layout.addLayout(author_layout)

# endregion Author Info

replied_message_text_field = QTextEdit()
replied_message_text_field.setPlaceholderText("Replied message text:")
replied_message_text_field.setMinimumHeight(48)
replied_message_text_field.textChanged.connect(update_markdown)
replied_message_info_layout.addWidget(replied_message_text_field)

message_link_field = QLineEdit()
message_link_field.setPlaceholderText("Link to replied message:")
message_link_field.textChanged.connect(update_markdown)
replied_message_info_layout.addWidget(message_link_field)

message_text_field = QTextEdit()
message_text_field.setPlaceholderText("Your reply:")
message_text_field.textChanged.connect(update_markdown)
replied_message_info_layout.addWidget(message_text_field)

main_layout.addLayout(replied_message_info_layout)

# endregion Replied Message Info

# endregion Message Info

preview_layout = QVBoxLayout()

preview_text_browser = QTextBrowser()
preview_layout.addWidget(preview_text_browser)

copy_button = QPushButton("Copy")
copy_button.pressed.connect(copy_to_clipboard)
preview_layout.addWidget(copy_button)

main_layout.addLayout(preview_layout)

main_widget.setLayout(main_layout)

window.setCentralWidget(main_widget)

window.show()
app.exec()
