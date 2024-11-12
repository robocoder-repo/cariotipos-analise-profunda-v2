
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class KaryotypeAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None

    def initUI(self):
        self.setWindowTitle('Karyotype Analyzer')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.load_button = QPushButton('Load Image')
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        self.analyze_button = QPushButton('Analyze Karyotype')
        self.analyze_button.clicked.connect(self.analyze_karyotype)
        layout.addWidget(self.analyze_button)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        self.result_label = QLabel('Results will appear here')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image(self.image)

    def display_image(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap.scaled(300, 200, Qt.KeepAspectRatio))

    def analyze_karyotype(self):
        if self.image is None:
            self.result_label.setText('Please load an image first')
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours based on area to remove small noise
        min_area = 100
        chromosomes = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        chromosome_count = len(chromosomes)
        
        result = f"Detected {chromosome_count} chromosomes."
        if chromosome_count == 46:
            result += " This appears to be a normal human karyotype."
        elif chromosome_count < 46:
            result += " This may indicate chromosomal deletion or loss."
        elif chromosome_count > 46:
            result += " This may indicate chromosomal duplication or gain."
        
        self.result_label.setText(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KaryotypeAnalyzer()
    ex.show()
    sys.exit(app.exec_())
