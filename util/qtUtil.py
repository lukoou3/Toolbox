import os

from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QImage

def getClipboardText():
    clipboard = QApplication.clipboard()
    return clipboard.text()

def setClipboardText(text):
    clipboard = QApplication.clipboard()
    return clipboard.setText(text)

def convert_png():
    filepath = r"icon"
    if not os.path.exists(filepath):
        print("目录不存在!")
        return
    filenames = os.listdir(filepath)
    for name in filenames:
        if name.endswith(".png"):
            path = filepath + '/' + name
            img = QImage()
            img.load(path);
            img.save(path);


if __name__ == '__main__':
    convert_png()



