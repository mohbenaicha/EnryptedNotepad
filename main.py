import sys
import os
import json
import base64
import datetime
import random
import string

from PyQt6.QtWidgets import (
    QApplication, QDialog, QHBoxLayout, QPushButton
)
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QTimer

from ui_main import MainWindowUI, CustomDialog, CustomMessageDialog
import encryption

NOTES_DIR = "notes"
CONFIG_FILE = "config.json"

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class EncryptedNotesApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindowUI()
        self.key = None
        self.password_verified = False
        os.makedirs(NOTES_DIR, exist_ok=True)
        self.config = encryption.load_config(CONFIG_FILE)
        self.auto_save_timer = QTimer()
        self.auto_save_timer.setInterval(3000)  # 3 seconds
        self.auto_save_timer.setSingleShot(True)
        self.last_saved_content = None

    def run(self):
        if not self.config:
            # First time setup: ask to set password
            if not self.set_password_dialog():
                return
        else:
            # Existing user: ask password to unlock
            if not self.login_dialog():
                return

        self.load_notes()
        self.disable_text_edit()  # Ensure text area is disabled until a note is selected
        self.setup_connections()
        self.window.show()
        self.auto_save_timer.timeout.connect(self.auto_save)
        sys.exit(self.app.exec())

    def set_password_dialog(self):
        dialog = CustomDialog(self.window, "Set Password", "Set a password to encrypt your notes:")
        dialog.input_field.setEchoMode(QLineEdit.EchoMode.Password)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            password = dialog.get_text()
            if not password:
                return False
            pw_hash = encryption.create_password_hash(password)
            encryption.save_config(pw_hash, CONFIG_FILE)
            self.key = encryption.derive_key(password, base64.b64decode(pw_hash['salt']))
            self.password_verified = True
            return True
        return False

    def login_dialog(self):
        for _ in range(3):
            dialog = CustomDialog(self.window, "Enter Password", "Enter password to unlock:")
            dialog.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                password = dialog.get_text()
                if not password:
                    return False
                salt = base64.b64decode(self.config['salt'])
                stored_hash = base64.b64decode(self.config['hash'])
                if encryption.verify_password(password, salt, stored_hash):
                    self.key = encryption.derive_key(password, salt)
                    self.password_verified = True
                    return True
                else:
                    dialog = CustomMessageDialog(self.window, "Incorrect Password", "Password incorrect. Try again.")
                    dialog.exec()
            else:
                return False
        return False

    def load_notes(self):
        self.notes = []
        self.window.list_widget.clear()
        for fname in sorted(os.listdir(NOTES_DIR), reverse=True):
            if fname.endswith('.enc'):
                try:
                    path = os.path.join(NOTES_DIR, fname)
                    with open(path, 'rb') as f:
                        encrypted = f.read()
                    decrypted = encryption.decrypt_data(self.key, encrypted).decode('utf-8')
                    first_line = decrypted.splitlines()[0].strip()
                    title = first_line[1:].strip() if first_line.startswith('#') else "Untitled"
                    self.notes.append({'filename': fname, 'title': title})
                    self.window.list_widget.addItem(title)
                except Exception:
                    pass

    def select_note_in_list(self, filename):
        for i in range(self.window.list_widget.count()):
            if self.notes[i]['filename'] == filename:
                self.window.list_widget.setCurrentRow(i)
                self.load_note(self.window.list_widget.currentItem())
                break

    def load_note(self, item):
        idx = self.window.list_widget.row(item)
        note = self.notes[idx]
        try:
            with open(os.path.join(NOTES_DIR, note['filename']), 'rb') as f:
                encrypted = f.read()
            decrypted = encryption.decrypt_data(self.key, encrypted).decode('utf-8')
            lines = decrypted.splitlines()
            if lines and lines[0].startswith('#'):
                content = '\n'.join(lines[1:]).lstrip('\n')
            else:
                content = decrypted
            self.current_filename = note['filename']
            self.window.text_edit.setReadOnly(False)
            self.window.text_edit.setHtml(content)
            self.auto_save()
        except Exception as e:
            dialog = CustomMessageDialog(self.window, "Error", f"Failed to load note: {e}")
            dialog.exec()

    def disable_text_edit(self):
        self.window.text_edit.setReadOnly(True)
        self.window.text_edit.clear()
        if hasattr(self, 'current_filename'):
            delattr(self, 'current_filename')

    def save_current_note(self, auto=False):
        if not hasattr(self, 'current_filename'):
            if not auto:
                dialog = CustomMessageDialog(self.window, "No Note Selected", "Please select or create a note first.")
                dialog.exec()
            return
        title = self.notes[self.window.list_widget.currentRow()]['title']
        content = self.window.text_edit.toHtml()
        full_content = f"# {title}\n\n{content}"
        enc_data = encryption.encrypt_data(self.key, full_content.encode('utf-8'))
        try:
            with open(os.path.join(NOTES_DIR, self.current_filename), 'wb') as f:
                f.write(enc_data)
            self.last_saved_content = content
            if not auto:
                dialog = CustomMessageDialog(self.window, "Saved", "Note saved successfully.")
                dialog.exec()
        except Exception as e:
            if not auto:
                dialog = CustomMessageDialog(self.window, "Error", f"Failed to save note: {e}")
                dialog.exec()

    def create_new_note(self):
        dialog = CustomDialog(self.window, "Create New Note", "Enter a title for the new note:")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            title = dialog.get_text()
            if not title:
                msg_dialog = CustomMessageDialog(self.window, "Empty Title", "Please enter a title for the new note.")
                msg_dialog.exec()
                return
            date_str = datetime.datetime.now().strftime("%Y%m%d")
            rand_str = random_string(6)
            filename = f"{date_str}_{rand_str}.enc"
            content = f"# {title}\n\n<p></p>"
            enc_data = encryption.encrypt_data(self.key, content.encode('utf-8'))
            with open(os.path.join(NOTES_DIR, filename), 'wb') as f:
                f.write(enc_data)
            self.load_notes()
            self.select_note_in_list(filename)

    def export_all_notes(self):
        from PyQt6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(self.window, "Select Export Folder")
        if not folder:
            return
        for note in self.notes:
            try:
                with open(os.path.join(NOTES_DIR, note['filename']), 'rb') as f:
                    encrypted = f.read()
                decrypted = encryption.decrypt_data(self.key, encrypted).decode('utf-8')
                lines = decrypted.splitlines()
                if lines and lines[0].startswith('#'):
                    content = '\n'.join(lines[1:]).lstrip('\n')
                else:
                    content = decrypted
                from PyQt6.QtGui import QTextDocument
                doc = QTextDocument()
                doc.setHtml(content)
                plain_text = doc.toPlainText()
                safe_title = ''.join(c for c in note['title'] if c.isalnum() or c in (' ', '_')).rstrip()
                export_name = f"{note['filename']}_{safe_title}.txt"
                export_path = os.path.join(folder, export_name)
                with open(export_path, 'w', encoding='utf-8') as ef:
                    ef.write(plain_text)
            except Exception:
                pass
        dialog = CustomMessageDialog(self.window, "Export Complete", "All notes exported successfully.")
        dialog.exec()

    def delete_note(self):
        if not hasattr(self, 'current_filename'):
            dialog = CustomMessageDialog(self.window, "No Note Selected", "Please select a note to delete.")
            dialog.exec()
            return
        
        current_row = self.window.list_widget.currentRow()
        if current_row < 0:
            dialog = CustomMessageDialog(self.window, "No Note Selected", "Please select a note to delete.")
            dialog.exec()
            return
        
        note = self.notes[current_row]
        title = note['title']
        
        # Show confirmation dialog
        confirm_dialog = CustomDialog(self.window, "Confirm Delete", f"Are you sure you want to delete '{title}'?\n\nThis action cannot be undone.")
        confirm_dialog.input_field.setVisible(False)
        confirm_dialog.input_field.setMaximumHeight(0)
        
        # Change button text for confirmation
        for child in confirm_dialog.children():
            if isinstance(child, QHBoxLayout):
                for i in range(child.count()):
                    widget = child.itemAt(i).widget()
                    if isinstance(widget, QPushButton):
                        if widget.text() == "Confirm":
                            widget.setText("Delete")
                            widget.setStyleSheet("""
                                QPushButton {
                                    background-color: #d9534f;
                                    border: none;
                                    padding: 8px 16px;
                                    border-radius: 8px;
                                    color: white;
                                    font-size: 13px;
                                }
                                QPushButton:hover {
                                    background-color: #c9302c;
                                }
                            """)
                        elif widget.text() == "Cancel":
                            widget.setText("Cancel")
        
        if confirm_dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Delete the file
                file_path = os.path.join(NOTES_DIR, note['filename'])
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                # Clear current note if it was the deleted one
                if hasattr(self, 'current_filename') and self.current_filename == note['filename']:
                    self.disable_text_edit()
                
                # Reload notes list
                self.load_notes()
                
                # Show success message
                success_dialog = CustomMessageDialog(self.window, "Note Deleted", f"'{title}' has been deleted successfully.")
                success_dialog.exec()
                
            except Exception as e:
                error_dialog = CustomMessageDialog(self.window, "Error", f"Failed to delete note: {e}")
                error_dialog.exec()

    def setup_connections(self):
        self.window.new_file_button.clicked.connect(self.create_new_note)
        self.window.save_button.clicked.connect(self.save_current_note)
        self.window.list_widget.itemClicked.connect(self.load_note)
        self.window.export_button.clicked.connect(self.export_all_notes)
        self.window.delete_button.clicked.connect(self.delete_note)
        self.window.text_edit.textChanged.connect(self.on_text_changed)

    def on_text_changed(self):
        self.auto_save_timer.stop()
        self.auto_save_timer.start()

    def auto_save(self):
        if not hasattr(self, 'current_filename'):
            return
        content = self.window.text_edit.toHtml()
        if content != self.last_saved_content:
            self.save_current_note(auto=True)

if __name__ == "__main__":
    app = EncryptedNotesApp()
    app.run()
