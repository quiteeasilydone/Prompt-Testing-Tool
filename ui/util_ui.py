from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로딩 중")
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setModal(True)

        # 로딩 이미지 설정
        self.loading_label = QLabel(self)
        pixmap = QPixmap(image_path)
        self.loading_label.setPixmap(pixmap)
        self.loading_label.setAlignment(Qt.AlignCenter)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.loading_label)
        self.setLayout(layout)

        # 창 크기를 이미지에 맞게 조정
        self.adjustSize()
