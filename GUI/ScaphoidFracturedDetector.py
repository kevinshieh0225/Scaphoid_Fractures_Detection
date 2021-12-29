from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os

import ScaphoidUI as ui

class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ImageLabelDictionary = {}
        self.FolderButton.clicked.connect(self.FolderButton_clicked)
        self.listView.clicked.connect(self.listView_clicked)
        self.ScapButton.clicked.connect(self.ScapButton_clicked)
        self.FracButton.clicked.connect(self.FracButton_clicked)

    def FolderButton_clicked(self):
        root= QFileDialog.getExistingDirectory()
        # img_path = os.path.join(root, 'images')
        antpath = os.path.join(root, 'Annotations')
        for type in ['Normal', 'Fracture']:
            imgpath = os.path.join(root, 'images', type)
            for filename in os.listdir(imgpath):
                if (filename.endswith(".bmp")):
                    name = filename.split('.')[0]
                    scaphoidannot = os.path.join(antpath, 'Scaphoid_Slice', f'{name}.json')
                    if os.path.exists(scaphoidannot) :
                        fractureannot = ''
                        if type == 'Fracture':
                            fractureannot = os.path.join(antpath, 'Fracture_Coordinate', f'{name}.csv')
                            if os.path.exists(fractureannot) :
                                continue
                        self.ImageLabelDictionary[name] = {
                            'imgpath': os.path.join(imgpath, filename), 
                            'type': type,
                            'scaphoidannot': scaphoidannot,
                            'fractureannot': fractureannot
                        }
                        slm = QStringListModel()
                        slm.setStringList(list(self.ImageLabelDictionary.keys()))
                        self.listView.setModel(slm)
                        
    def listView_clicked(self, qModelIndex):
        name = list(self.ImageLabelDictionary.keys())[qModelIndex.row()]
        # QMessageBox.information(self,'ListViewer','你選擇了:'+ name)
        imgpath = self.ImageLabelDictionary[name]['imgpath']
        pixmap = QPixmap(imgpath).scaled(self.SourceImg.width(), self.SourceImg.height(), Qt.KeepAspectRatio)
        self.SourceImg.setPixmap(pixmap)
        self.ProcessImg.setPixmap(pixmap)

    def ScapButton_clicked(self):
        pass
    def FracButton_clicked(self):
        pass

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())