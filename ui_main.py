from PyQt6.QtWidgets import (
    QWidget, QListWidget, QTextEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QFileDialog, QSplitter, QToolButton, QSplitterHandle, QFrame, QSlider, QApplication,
    QDialog, QMessageBox
)
from PyQt6.QtGui import QFont, QColor, QAction, QIcon, QPixmap, QPen, QTextCharFormat, QTextCursor, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QImage, QBrush
import sys

class CustomDialog(QDialog):
    def __init__(self, parent=None, title="", message=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(400, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #0b1a2d;
                color: white;
                border-radius: 12px;
                border: 2px solid #3366cc;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(35)
        title_bar.setStyleSheet("background: #12213a; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #aad8ff;")
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)
        
        close_btn = QToolButton()
        close_btn.setText("×")
        close_btn.setToolTip("Cancel")
        close_btn.setStyleSheet("""
            QToolButton {
                background: none; font-size: 16px; color: #aad8ff; border-radius: 6px;
            }
            QToolButton:hover {
                background: #d9534f; color: white;
            }
        """)
        close_btn.clicked.connect(self.reject)
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_bar)
        
        # Message
        if message:
            msg_label = QLabel(message)
            msg_label.setStyleSheet("color: #aad8ff; font-size: 13px; margin-bottom: 10px;")
            layout.addWidget(msg_label)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setMinimumHeight(40)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #102a4c;
                border: 2px solid #3366cc;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #aad8ff;
            }
        """)
        layout.addWidget(self.input_field)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a3a6d;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                color: white;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3366cc;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        confirm_btn = QPushButton("Confirm")
        confirm_btn.setMinimumHeight(35)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a3a6d;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                color: white;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3366cc;
            }
        """)
        confirm_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        layout.addLayout(button_layout)
        
        # Make dialog draggable
        self._drag_active = False
        self._drag_pos = None
        title_bar.mousePressEvent = self._title_mouse_press
        title_bar.mouseMoveEvent = self._title_mouse_move
        title_bar.mouseReleaseEvent = self._title_mouse_release
        
        # Set focus to input field
        self.input_field.setFocus()
        
        # Connect Enter key to confirm button
        self.input_field.returnPressed.connect(self.accept)
        
    def _title_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def _title_mouse_move(self, event):
        if self._drag_active and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
    
    def _title_mouse_release(self, event):
        self._drag_active = False
        event.accept()
    
    def get_text(self):
        return self.input_field.text().strip()

class CustomMessageDialog(QDialog):
    def __init__(self, parent=None, title="", message="", icon_type="info"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(400, 180)
        self.setStyleSheet("""
            QDialog {
                background-color: #0b1a2d;
                color: white;
                border-radius: 12px;
                border: 2px solid #3366cc;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(35)
        title_bar.setStyleSheet("background: #12213a; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #aad8ff;")
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)
        
        close_btn = QToolButton()
        close_btn.setText("×")
        close_btn.setToolTip("Close")
        close_btn.setStyleSheet("""
            QToolButton {
                background: none; font-size: 16px; color: #aad8ff; border-radius: 6px;
            }
            QToolButton:hover {
                background: #d9534f; color: white;
            }
        """)
        close_btn.clicked.connect(self.accept)
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_bar)
        
        # Message
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("color: #aad8ff; font-size: 13px; margin: 10px 0;")
        layout.addWidget(msg_label)
        
        # OK button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        ok_btn = QPushButton("OK")
        ok_btn.setMinimumHeight(35)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a3a6d;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                color: white;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3366cc;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(ok_btn)
        layout.addLayout(button_layout)
        
        # Make dialog draggable
        self._drag_active = False
        self._drag_pos = None
        title_bar.mousePressEvent = self._title_mouse_press
        title_bar.mouseMoveEvent = self._title_mouse_move
        title_bar.mouseReleaseEvent = self._title_mouse_release
        
    def _title_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def _title_mouse_move(self, event):
        if self._drag_active and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
    
    def _title_mouse_release(self, event):
        self._drag_active = False
        event.accept()

def colorize_icon(path, color):
    pixmap = QPixmap(path)
    image = pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
    for y in range(image.height()):
        for x in range(image.width()):
            alpha = image.pixelColor(x, y).alpha()
            if alpha > 0:
                image.setPixelColor(x, y, QColor(color.red(), color.green(), color.blue(), alpha))
    return QIcon(QPixmap.fromImage(image))

class CustomSplitterHandle(QSplitterHandle):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.setCursor(Qt.CursorShape.SplitHCursor)
        self.setMinimumWidth(18)
        self._hover = False

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self._hover:
            painter.setBrush(QColor(170, 216, 255, 40))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.rect())
        line_color = QColor('#aad8ff')
        painter.setPen(QPen(line_color, 4))
        x1 = w // 2 - 4
        x2 = w // 2 + 4
        y1 = h // 2 - min(12, h // 2 - 2)
        y2 = h // 2 + min(12, h // 2 - 2)
        painter.drawLine(x1, y1, x1, y2)
        painter.drawLine(x2, y1, x2, y2)

class CustomSplitter(QSplitter):
    def createHandle(self):
        return CustomSplitterHandle(self.orientation(), self)

class ResizeHandle(QFrame):
    def __init__(self, parent, position):
        super().__init__(parent)
        self.position = position  # e.g., 'left', 'right', 'top', 'bottom', 'topleft', etc.
        self.setMouseTracking(True)
        self.setStyleSheet("background: transparent;")
        self._hover = False

    def enterEvent(self, event):
        self._hover = True
        self.update()
        if self.position in ['left', 'right']:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif self.position in ['top', 'bottom']:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif self.position == 'topleft' or self.position == 'bottomright':
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif self.position == 'topright' or self.position == 'bottomleft':
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        if self._hover:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QColor(170, 216, 255, 60))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.rect())
        super().paintEvent(event)

class MainWindowUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encrypted Notes")
        self.resize(900, 600)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.setStyleSheet("""
            QWidget {
                background-color: #0b1a2d;
                color: white;
                font-family: 'Inter', 'Segoe UI Variable', 'Segoe UI', 'Roboto', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 15px;
                border-radius: 12px;
            }
            QListWidget {
                background-color: #102a4c;
                border: none;
                border-radius: 10px;
            }
            QTextEdit {
                background-color: #081229;
                border: none;
                color: white;
                border-radius: 10px;
            }
            QPushButton, QToolButton {
                background-color: #1a3a6d;
                border: none;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover, QToolButton:hover {
                background-color: #3366cc;
            }
            QLineEdit {
                background-color: #102a4c;
                border: none;
                color: white;
                padding: 6px;
                border-radius: 8px;
            }
            QLabel {
                color: #aad8ff;
                border-radius: 8px;
            }
        """)

        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(36)
        self.title_bar.setStyleSheet("background: #12213a; border-top-left-radius: 12px; border-top-right-radius: 12px;")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)
        self.title_label = QLabel("Encrypted Notes")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #aad8ff;")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch(1)
        self.min_btn = QToolButton()
        self.min_btn.setText("–")
        self.min_btn.setToolTip("Minimize")
        self.min_btn.setStyleSheet("""
            QToolButton {
                background: none; font-size: 18px; color: #aad8ff; border-radius: 6px;
            }
            QToolButton:hover {
                background: #224477;
            }
        """)
        self.close_btn = QToolButton()
        self.close_btn.setText("×")
        self.close_btn.setToolTip("Close")
        self.close_btn.setStyleSheet("""
            QToolButton {
                background: none; font-size: 18px; color: #aad8ff; border-radius: 6px;
            }
            QToolButton:hover {
                background: #d9534f; color: white;
            }
        """)
        title_layout.addWidget(self.min_btn)
        title_layout.addWidget(self.close_btn)

        main_splitter = CustomSplitter(Qt.Orientation.Horizontal)
        side_widget = QWidget()
        side_layout = QVBoxLayout(side_widget)
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)

        self.list_widget = QListWidget()

        bright_color = QColor(180, 220, 255)
        self.new_file_button = QToolButton()
        self.new_file_button.setIcon(colorize_icon("media/new.png", bright_color))
        self.new_file_button.setIconSize(QSize(20, 20))
        self.new_file_button.setToolTip("Create New Note")
        self.new_file_button.setText("")
        self.new_file_button.setAutoRaise(True)

        side_layout.addWidget(QLabel("Notes"))
        side_layout.addWidget(self.list_widget)
        side_layout.addWidget(self.new_file_button)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.save_button = QToolButton()
        self.save_button.setIcon(colorize_icon("media/save.png", bright_color))
        self.save_button.setIconSize(QSize(20, 20))
        self.save_button.setToolTip("Save Note")
        self.save_button.setAutoRaise(True)
        self.export_button = QToolButton()
        self.export_button.setIcon(colorize_icon("media/export.png", bright_color))
        self.export_button.setIconSize(QSize(20, 20))
        self.export_button.setToolTip("Export All Notes")
        self.export_button.setAutoRaise(True)

        self.delete_button = QToolButton()
        self.delete_button.setText("🗑")
        self.delete_button.setIconSize(QSize(20, 20))
        self.delete_button.setToolTip("Delete Selected Note")
        self.delete_button.setAutoRaise(True)
        self.delete_button.setStyleSheet("""
            QToolButton {
                background-color: #1a3a6d;
                border: none;
                padding: 8px;
                border-radius: 8px;
                color: #ff6b6b;
                font-size: 16px;
            }
            QToolButton:hover {
                background-color: #d9534f;
                color: white;
            }
        """)

        self.ui_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.ui_scale_slider.setMinimum(80)
        self.ui_scale_slider.setMaximum(300)
        self.ui_scale_slider.setValue(100)
        self.ui_scale_slider.setFixedWidth(120)
        self.ui_scale_slider.setFixedHeight(20)
        self.ui_scale_slider.setMinimumHeight(20)
        self.ui_scale_slider.setMaximumHeight(20)
        self.ui_scale_slider.setToolTip("UI Scale")
        self.ui_scale_slider.valueChanged.connect(self._update_ui_scale)
        self.ui_scale_slider.setStyleSheet('''
            QSlider {
                background: transparent;
                border-radius: 10px;
                padding: 0 4px;
            }
            QSlider::groove:horizontal {
                border: 1.5px solid #3366cc;
                height: 5px;
                background: #1a3a6d;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #aad8ff;
                border: 3px solid #3366cc;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #66b3ff;
                border: 3px solid #aad8ff;
            }
        ''')

        self.slider_minus = QLabel("−")
        self.slider_minus.setStyleSheet("color: #aad8ff; font-size: 16px; padding-right: 2px;")
        self.slider_plus = QLabel("+")
        self.slider_plus.setStyleSheet("color: #aad8ff; font-size: 16px; padding-left: 2px;")
        self.slider_group = QHBoxLayout()
        self.slider_group.setContentsMargins(0, 0, 0, 0)
        self.slider_group.setSpacing(0)
        self.slider_group.addWidget(self.slider_minus)
        self.slider_group.addWidget(self.ui_scale_slider)
        self.slider_group.addWidget(self.slider_plus)
        self.slider_group_widget = QWidget()
        self.slider_group_widget.setLayout(self.slider_group)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.new_file_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.slider_group_widget)
        button_layout.setSpacing(8)
        button_layout.setContentsMargins(0, 0, 12, 0)

        self.format_toolbar = QHBoxLayout()
        self.format_toolbar.setContentsMargins(0, 0, 0, 0)
        self.format_toolbar.setSpacing(4)
        self.bold_btn = QToolButton()
        self.bold_btn.setText('B')
        self.bold_btn.setToolTip('Bold')
        self.bold_btn.setCheckable(True)
        self.bold_btn.setStyleSheet('''
            QToolButton {
                font-weight: bold;
                font-size: 16px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QToolButton:hover { background: #3366cc; color: #fff; }
        ''')
        self.italic_btn = QToolButton()
        self.italic_btn.setText('I')
        self.italic_btn.setToolTip('Italic')
        self.italic_btn.setCheckable(True)
        self.italic_btn.setStyleSheet('''
            QToolButton {
                font-style: italic;
                font-size: 16px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QToolButton:hover { background: #3366cc; color: #fff; }
        ''')
        self.underline_btn = QToolButton()
        self.underline_btn.setText('U')
        self.underline_btn.setToolTip('Underline')
        self.underline_btn.setCheckable(True)
        self.underline_btn.setStyleSheet('''
            QToolButton {
                text-decoration: underline;
                font-size: 16px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QToolButton:hover { background: #3366cc; color: #fff; }
        ''')
        self.format_toolbar.addWidget(self.bold_btn)
        self.format_toolbar.addWidget(self.italic_btn)
        self.format_toolbar.addWidget(self.underline_btn)
        self.h1_btn = QToolButton()
        self.h1_btn.setText('H1')
        self.h1_btn.setToolTip('Heading 1')
        self.h1_btn.setStyleSheet('''
            QToolButton {
                font-weight: bold;
                font-size: 16px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QToolButton:hover { background: #3366cc; color: #fff; }
        ''')
        self.h2_btn = QToolButton()
        self.h2_btn.setText('H2')
        self.h2_btn.setToolTip('Heading 2')
        self.h2_btn.setStyleSheet('''
            QToolButton {
                font-weight: bold;
                font-size: 16px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QToolButton:hover { background: #3366cc; color: #fff; }
        ''')
        self.h3_btn = QToolButton()
        self.h3_btn.setText('H3')
        self.h3_btn.setToolTip('Heading 3')
        self.h3_btn.setStyleSheet('''
            QToolButton {
                font-weight: bold;
                font-size: 16px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QToolButton:hover { background: #3366cc; color: #fff; }
        ''')
        self.format_toolbar.addWidget(self.h1_btn)
        self.format_toolbar.addWidget(self.h2_btn)
        self.format_toolbar.addWidget(self.h3_btn)
        # Normal button
        self.normal_btn = QToolButton()
        self.normal_btn.setText('Tx')
        self.normal_btn.setToolTip('Normal Text')
        self.normal_btn.setStyleSheet('''
            QToolButton {
                font-size: 16px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: 32px;
                min-height: 32px;
                max-width: 32px;
                max-height: 32px;
            }
            QToolButton:hover { background: #3366cc; color: #fff; }
        ''')
        self.format_toolbar.addWidget(self.normal_btn)
        self.format_toolbar.addStretch(1)
        # Insert the toolbar above the text area
        editor_layout.insertLayout(0, self.format_toolbar)

        editor_layout.addWidget(self.text_edit)
        editor_layout.addLayout(button_layout)
        editor_layout.setStretch(0, 1)  # Make QTextEdit expand
        editor_layout.setStretch(1, 0)  # Button bar does not expand

        main_splitter.addWidget(side_widget)
        main_splitter.addWidget(editor_widget)
        main_splitter.setSizes([270, 630])  # 30%/70% split
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(main_splitter)

        self.close_btn.clicked.connect(self.close)
        self.min_btn.clicked.connect(self.showMinimized)
        # Variables for dragging
        self._drag_active = False
        self._drag_pos = None
        self.title_bar.mousePressEvent = self._title_mouse_press
        self.title_bar.mouseMoveEvent = self._title_mouse_move
        self.title_bar.mouseReleaseEvent = self._title_mouse_release
        # --- Custom window resizing logic ---
        self._resize_margin = 4
        self._resizing = False
        self._resize_dir = None
        self.setMouseTracking(True)
        # --- Custom resize handles ---
        self._handles = {}
        for pos in ['left', 'right', 'top', 'bottom', 'topleft', 'topright', 'bottomleft', 'bottomright']:
            handle = ResizeHandle(self, pos)
            handle.installEventFilter(self)
            handle.raise_()
            handle.show()
            self._handles[pos] = handle
        self._resize_active = False
        self._resize_start_geom = None
        self._resize_start_pos = None
        self._handle_size = 8
        self._update_handles()
        # Store scale factor
        self._ui_scale = 1.0

        # At the top of the file, before any widgets are created
        app = QApplication.instance() or QApplication(sys.argv)
        app.setStyle("Fusion")

        # After creating self.list_widget and self.text_edit
        scrollbar_style = """
QScrollBar:vertical, QScrollBar:horizontal {
    background: transparent;
    border: none;
    box-shadow: none;
    width: 12px;
    height: 12px;
    margin: 0px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #aad8ff;
    border: none;
    border-radius: 6px;
    box-shadow: none;
    min-height: 32px;
    min-width: 32px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: transparent;
    border: none;
    box-shadow: none;
    height: 16px;
    width: 16px;
    border-radius: 8px;
}
QScrollBar::up-arrow, QScrollBar::down-arrow, QScrollBar::left-arrow, QScrollBar::right-arrow {
    background: transparent;
    border: none;
    box-shadow: none;
    width: 10px;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::up-arrow {
    image: url(data:image/svg+xml;utf8,<svg width='10' height='10' xmlns='http://www.w3.org/2000/svg'><polygon points='5,2 9,8 1,8' fill='%2366b3ff'/></svg>);
}
QScrollBar::down-arrow {
    image: url(data:image/svg+xml;utf8,<svg width='10' height='10' xmlns='http://www.w3.org/2000/svg'><polygon points='5,8 9,2 1,2' fill='%2366b3ff'/></svg>);
}
QScrollBar::left-arrow {
    image: url(data:image/svg+xml;utf8,<svg width='10' height='10' xmlns='http://www.w3.org/2000/svg'><polygon points='2,5 8,9 8,1' fill='%2366b3ff'/></svg>);
}
QScrollBar::right-arrow {
    image: url(data:image/svg+xml;utf8,<svg width='10' height='10' xmlns='http://www.w3.org/2000/svg'><polygon points='8,5 2,9 2,1' fill='%2366b3ff'/></svg>);
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
    border: none;
    box-shadow: none;
}
"""
        self.list_widget.setStyleSheet(scrollbar_style)
        self.text_edit.setStyleSheet(scrollbar_style)

        # Connect formatting buttons
        self.bold_btn.clicked.connect(self.toggle_bold)
        self.italic_btn.clicked.connect(self.toggle_italic)
        self.underline_btn.clicked.connect(self.toggle_underline)
        self.text_edit.cursorPositionChanged.connect(self.update_format_buttons)
        self.h1_btn.clicked.connect(lambda: self.set_heading(28))
        self.h2_btn.clicked.connect(lambda: self.set_heading(22))
        self.h3_btn.clicked.connect(lambda: self.set_heading(16))
        self.normal_btn.clicked.connect(self.set_normal_text)

        # Shortcuts for formatting and file actions
        QShortcut(QKeySequence('Ctrl+B'), self, activated=self.bold_btn.click)
        QShortcut(QKeySequence('Ctrl+I'), self, activated=self.italic_btn.click)
        QShortcut(QKeySequence('Ctrl+U'), self, activated=self.underline_btn.click)
        QShortcut(QKeySequence('Ctrl+N'), self, activated=self.new_file_button.click)
        QShortcut(QKeySequence('Ctrl+S'), self, activated=self.save_button.click)
        QShortcut(QKeySequence('Ctrl+E'), self, activated=self.export_button.click)
        QShortcut(QKeySequence('Delete'), self, activated=self.delete_button.click)
        # Underline leading spaces workaround
        self._block_underline_leading_spaces = False

    def _title_mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def _title_mouse_move(self, event):
        if self._drag_active and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def _title_mouse_release(self, event):
        self._drag_active = False
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            margin = self._resize_margin
            pos = event.position().toPoint()
            rect = self.rect()
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            # Determine which edge/corner is being pressed
            if x <= pos.x() <= x + margin:
                if y <= pos.y() <= y + margin:
                    self._resize_dir = 'topleft'
                elif y + h - margin <= pos.y() <= y + h:
                    self._resize_dir = 'bottomleft'
                else:
                    self._resize_dir = 'left'
            elif x + w - margin <= pos.x() <= x + w:
                if y <= pos.y() <= y + margin:
                    self._resize_dir = 'topright'
                elif y + h - margin <= pos.y() <= y + h:
                    self._resize_dir = 'bottomright'
                else:
                    self._resize_dir = 'right'
            elif y <= pos.y() <= y + margin:
                self._resize_dir = 'top'
            elif y + h - margin <= pos.y() <= y + h:
                self._resize_dir = 'bottom'
            else:
                self._resize_dir = None
            if self._resize_dir:
                self._resizing = True
                self._resize_start_geom = self.geometry()
                self._resize_start_pos = event.globalPosition().toPoint()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        margin = self._resize_margin
        pos = event.position().toPoint()
        rect = self.rect()
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        cursor_set = False
        if not self._resizing:
            if x <= pos.x() <= x + margin:
                if y <= pos.y() <= y + margin:
                    self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                    cursor_set = True
                elif y + h - margin <= pos.y() <= y + h:
                    self.setCursor(Qt.CursorShape.SizeBDiagCursor)
                    cursor_set = True
                else:
                    self.setCursor(Qt.CursorShape.SizeHorCursor)
                    cursor_set = True
            elif x + w - margin <= pos.x() <= x + w:
                if y <= pos.y() <= y + margin:
                    self.setCursor(Qt.CursorShape.SizeBDiagCursor)
                    cursor_set = True
                elif y + h - margin <= pos.y() <= y + h:
                    self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                    cursor_set = True
                else:
                    self.setCursor(Qt.CursorShape.SizeHorCursor)
                    cursor_set = True
            elif y <= pos.y() <= y + margin:
                self.setCursor(Qt.CursorShape.SizeVerCursor)
                cursor_set = True
            elif y + h - margin <= pos.y() <= y + h:
                self.setCursor(Qt.CursorShape.SizeVerCursor)
                cursor_set = True
            if not cursor_set:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        if self._resizing:
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            geom = self._resize_start_geom
            new_geom = geom
            if self._resize_dir == 'left':
                new_geom.setLeft(geom.left() + delta.x())
            elif self._resize_dir == 'right':
                new_geom.setRight(geom.right() + delta.x())
            elif self._resize_dir == 'top':
                new_geom.setTop(geom.top() + delta.y())
            elif self._resize_dir == 'bottom':
                new_geom.setBottom(geom.bottom() + delta.y())
            elif self._resize_dir == 'topleft':
                new_geom.setTop(geom.top() + delta.y())
                new_geom.setLeft(geom.left() + delta.x())
            elif self._resize_dir == 'topright':
                new_geom.setTop(geom.top() + delta.y())
                new_geom.setRight(geom.right() + delta.x())
            elif self._resize_dir == 'bottomleft':
                new_geom.setBottom(geom.bottom() + delta.y())
                new_geom.setLeft(geom.left() + delta.x())
            elif self._resize_dir == 'bottomright':
                new_geom.setBottom(geom.bottom() + delta.y())
                new_geom.setRight(geom.right() + delta.x())
            self.setGeometry(new_geom)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_dir = None
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_handles()

    def _update_handles(self):
        w, h, s = self.width(), self.height(), self._handle_size
        # Edges
        self._handles['left'].setGeometry(0, s, s, h-2*s)
        self._handles['right'].setGeometry(w-s, s, s, h-2*s)
        self._handles['top'].setGeometry(s, 0, w-2*s, s)
        self._handles['bottom'].setGeometry(s, h-s, w-2*s, s)
        # Corners
        self._handles['topleft'].setGeometry(0, 0, s, s)
        self._handles['topright'].setGeometry(w-s, 0, s, s)
        self._handles['bottomleft'].setGeometry(0, h-s, s, s)
        self._handles['bottomright'].setGeometry(w-s, h-s, s, s)

    def eventFilter(self, obj, event):
        if isinstance(obj, ResizeHandle):
            if event.type() == event.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                self._resize_active = True
                self._resize_dir = obj.position
                self._resize_start_geom = self.geometry()
                self._resize_start_pos = event.globalPosition().toPoint()
                return True
            elif event.type() == event.Type.MouseMove and self._resize_active:
                delta = event.globalPosition().toPoint() - self._resize_start_pos
                geom = self._resize_start_geom
                new_geom = geom.getRect()  # returns (x, y, w, h)
                x, y, w, h = new_geom
                min_w, min_h = 400, 300
                if self._resize_dir == 'left':
                    new_x = min(x + delta.x(), x + w - min_w)
                    new_w = max(w - delta.x(), min_w)
                    self.setGeometry(new_x, y, new_w, h)
                elif self._resize_dir == 'right':
                    new_w = max(w + delta.x(), min_w)
                    self.setGeometry(x, y, new_w, h)
                elif self._resize_dir == 'top':
                    new_y = min(y + delta.y(), y + h - min_h)
                    new_h = max(h - delta.y(), min_h)
                    self.setGeometry(x, new_y, w, new_h)
                elif self._resize_dir == 'bottom':
                    new_h = max(h + delta.y(), min_h)
                    self.setGeometry(x, y, w, new_h)
                elif self._resize_dir == 'topleft':
                    new_x = min(x + delta.x(), x + w - min_w)
                    new_w = max(w - delta.x(), min_w)
                    new_y = min(y + delta.y(), y + h - min_h)
                    new_h = max(h - delta.y(), min_h)
                    self.setGeometry(new_x, new_y, new_w, new_h)
                elif self._resize_dir == 'topright':
                    new_w = max(w + delta.x(), min_w)
                    new_y = min(y + delta.y(), y + h - min_h)
                    new_h = max(h - delta.y(), min_h)
                    self.setGeometry(x, new_y, new_w, new_h)
                elif self._resize_dir == 'bottomleft':
                    new_x = min(x + delta.x(), x + w - min_w)
                    new_w = max(w - delta.x(), min_w)
                    new_h = max(h + delta.y(), min_h)
                    self.setGeometry(new_x, y, new_w, new_h)
                elif self._resize_dir == 'bottomright':
                    new_w = max(w + delta.x(), min_w)
                    new_h = max(h + delta.y(), min_h)
                    self.setGeometry(x, y, new_w, new_h)
                return True
            elif event.type() == event.Type.MouseButtonRelease:
                self._resize_active = False
                self._resize_dir = None
                return True
        return super().eventFilter(obj, event)

    def _update_ui_scale(self, value):
        self._ui_scale = value / 100.0
        scale = self._ui_scale
        # Update stylesheet with scaled values
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #0b1a2d;
                color: white;
                font-family: 'Inter', 'Segoe UI Variable', 'Segoe UI', 'Roboto', Tahoma, Geneva, Verdana, sans-serif;
                font-size: {int(15*scale)}px;
                border-radius: {int(12*scale)}px;
            }}
            QListWidget {{
                background-color: #102a4c;
                border: none;
                border-radius: {int(10*scale)}px;
            }}
            QTextEdit {{
                background-color: #081229;
                border: none;
                color: white;
                border-radius: {int(10*scale)}px;
            }}
            QPushButton, QToolButton {{
                background-color: #1a3a6d;
                border: none;
                padding: {int(8*scale)}px;
                border-radius: {int(8*scale)}px;
            }}
            QPushButton:hover, QToolButton:hover {{
                background-color: #3366cc;
            }}
            QLineEdit {{
                background-color: #102a4c;
                border: none;
                color: white;
                padding: {int(6*scale)}px;
                border-radius: {int(8*scale)}px;
            }}
            QLabel {{
                color: #aad8ff;
                border-radius: {int(8*scale)}px;
            }}
        """)
        # Update icon sizes
        icon_size = int(20 * scale)
        self.new_file_button.setIconSize(QSize(icon_size, icon_size))
        self.save_button.setIconSize(QSize(icon_size, icon_size))
        self.export_button.setIconSize(QSize(icon_size, icon_size))
        self.delete_button.setIconSize(QSize(icon_size, icon_size))
        # Update title bar height
        self.title_bar.setFixedHeight(int(36*scale))
        self.title_label.setStyleSheet(f"font-weight: bold; font-size: {int(16*scale)}px; color: #aad8ff;")
        self.min_btn.setStyleSheet(f"""
            QToolButton {{
                background: none; font-size: {int(18*scale)}px; color: #aad8ff; border-radius: {int(6*scale)}px;
            }}
            QToolButton:hover {{
                background: #224477;
            }}
        """)
        self.close_btn.setStyleSheet(f"""
            QToolButton {{
                background: none; font-size: {int(18*scale)}px; color: #aad8ff; border-radius: {int(6*scale)}px;
            }}
            QToolButton:hover {{
                background: #d9534f; color: white;
            }}
        """)
        # Update splitter handle width
        for widget in self.findChildren(QSplitterHandle):
            widget.setMinimumWidth(int(18*scale))
        # Update resize handle size
        self._handle_size = int(8*scale)
        self._update_handles()
        # Update QTextEdit font size
        font = self.text_edit.font()
        font.setPointSizeF(14 * scale)
        self.text_edit.setFont(font)
        # Update formatting toolbar button font sizes
        button_size = int(32 * scale)
        button_font = int(16 * scale)
        button_style = f'''
            QToolButton {{
                font-weight: bold;
                font-size: {button_font}px;
                color: #aad8ff;
                background: #12213a;
                border-radius: 6px;
                padding: 2px 6px;
                min-width: {button_size}px;
                min-height: {button_size}px;
                max-width: {button_size}px;
                max-height: {button_size}px;
            }}
            QToolButton:hover {{ background: #3366cc; color: #fff; }}
        '''
        self.bold_btn.setStyleSheet(button_style)
        self.italic_btn.setStyleSheet(button_style)
        self.underline_btn.setStyleSheet(button_style)
        self.h1_btn.setStyleSheet(button_style)
        self.h2_btn.setStyleSheet(button_style)
        self.h3_btn.setStyleSheet(button_style)
        self.normal_btn.setStyleSheet(button_style)
        # Update all text in QTextEdit to scale font size
        doc = self.text_edit.document()
        cursor = QTextCursor(doc)
        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setFontPointSize(14 * scale)
        cursor.mergeCharFormat(fmt)

    def toggle_bold(self):
        fmt = QTextCharFormat()
        from PyQt6.QtGui import QFont
        fmt.setFontWeight(QFont.Weight.Bold if self.bold_btn.isChecked() else QFont.Weight.Normal)
        self.merge_format_on_selection(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_btn.isChecked())
        self.merge_format_on_selection(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_btn.isChecked())
        self.merge_format_on_selection(fmt)

    def merge_format_on_selection(self, fmt):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.text_edit.mergeCurrentCharFormat(fmt)

    def update_format_buttons(self):
        fmt = self.text_edit.currentCharFormat()
        self.bold_btn.setChecked(fmt.fontWeight() > 50)
        self.italic_btn.setChecked(fmt.fontItalic())
        self.underline_btn.setChecked(fmt.fontUnderline())

    def _underline_leading_spaces(self):
        if self._block_underline_leading_spaces:
            return
        self._block_underline_leading_spaces = True
        try:
            cursor = self.text_edit.textCursor()
            block = cursor.block()
            text = block.text()
            if text and text[0] == ' ':
                cursor_pos = cursor.position()
                block_pos = block.position()
                cursor.beginEditBlock()
                for i, ch in enumerate(text):
                    if ch != ' ':
                        break
                    cursor.setPosition(block_pos + i)
                    cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
                    fmt = QTextCharFormat()
                    fmt.setFontUnderline(True)
                    cursor.mergeCharFormat(fmt)
                cursor.endEditBlock()
                cursor.setPosition(cursor_pos)
                self.text_edit.setTextCursor(cursor)
        finally:
            self._block_underline_leading_spaces = False

    def set_heading(self, size):
        cursor = self.text_edit.textCursor()
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        fmt.setFontWeight(QFont.Weight.Bold)
        if cursor.hasSelection():
            cursor.mergeCharFormat(fmt)
        else:
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            cursor.mergeCharFormat(fmt)
        self.text_edit.mergeCurrentCharFormat(fmt)

    def set_normal_text(self):
        cursor = self.text_edit.textCursor()
        fmt = QTextCharFormat()
        fmt.setFontPointSize(14)
        fmt.setFontWeight(QFont.Weight.Normal)
        if cursor.hasSelection():
            cursor.mergeCharFormat(fmt)
        else:
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            cursor.mergeCharFormat(fmt)
        self.text_edit.mergeCurrentCharFormat(fmt)
