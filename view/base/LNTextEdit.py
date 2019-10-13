'''
Text widget with support for line numbers
Downloaded from: http://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/
Updated to be compatible with python 3.
'''
import sys
from PyQt5.Qt import QFrame
from PyQt5.Qt import QHBoxLayout
from PyQt5.Qt import QPainter
from PyQt5.Qt import QPlainTextEdit
from PyQt5.Qt import QRect
from PyQt5.Qt import QTextEdit
from PyQt5.Qt import QTextFormat
from PyQt5.Qt import QWidget
from PyQt5.Qt import Qt
from quamash import QApplication


class LNTextEdit(QFrame):
    class NumberBar(QWidget):

        def __init__(self, edit):
            QWidget.__init__(self, edit)

            self.edit = edit
            self.adjustWidth(1)

        def paintEvent(self, event):
            self.edit.numberbarPaint(self, event)
            QWidget.paintEvent(self, event)

        def adjustWidth(self, count):
            width = self.fontMetrics().width(str(count))
            if self.width() != width:
                self.setFixedWidth(width)

        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                # It would be nice to do
                # self.update(0, rect.y(), self.width(), rect.height())
                # But we can't because it will not remove the bold on the
                # current line if word wrap is enabled and a new block is
                # selected.
                self.update()

    class PlainTextEdit(QPlainTextEdit):

        def __init__(self, *args):
            QPlainTextEdit.__init__(self, *args)

            # self.setFrameStyle(QFrame.NoFrame)

            self.setFrameStyle(QFrame.NoFrame)
            self.highlight()
            # self.setLineWrapMode(QPlainTextEdit.NoWrap)

            self.cursorPositionChanged.connect(self.highlight)

        def highlight(self):
            hi_selection = QTextEdit.ExtraSelection()

            hi_selection.format.setBackground(self.palette().alternateBase())
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()

            self.setExtraSelections([hi_selection])

        def numberbarPaint(self, number_bar, event):
            font_metrics = self.fontMetrics()
            current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1

            block = self.firstVisibleBlock()
            line_count = block.blockNumber()
            painter = QPainter(number_bar)
            painter.fillRect(event.rect(), self.palette().base())

            # Iterate over all visible text blocks in the document.
            while block.isValid():
                line_count += 1
                block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

                # Check if the position of the block is out side of the visible
                # area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break

                # We want the line number for the selected line to be bold.
                if line_count == current_line:
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
                else:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)

                # Draw the line number right justified at the position of the line.
                paint_rect = QRect(0, block_top, number_bar.width(), font_metrics.height())
                painter.drawText(paint_rect, Qt.AlignRight, str(line_count))

                block = block.next()

            painter.end()

    def __init__(self, *args):
        QFrame.__init__(self, *args)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        self.edit = self.PlainTextEdit()
        self.number_bar = self.NumberBar(self.edit)

        self.highlighterclass = None
        self.highlighter = None

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)

        self.edit.blockCountChanged.connect(self.number_bar.adjustWidth)
        self.edit.updateRequest.connect(self.number_bar.updateContents)

    def getText(self):
        return self.edit.toPlainText()

    def setText(self, text):
        self.edit.setPlainText(text)

        # Qt bug prevents highlighter to work after a few sets...
        # This work-around seems to 'fix' that.
        self.setHighlighterClass(self.highlighterclass)

    def isModified(self):
        return self.edit.document().isModified()

    def setModified(self, modified):
        self.edit.document().setModified(modified)

    def setLineWrapMode(self, mode):
        self.edit.setLineWrapMode(mode)

    def setHighlighterClass(self, highlighterclass):
        self.highlighterclass = highlighterclass
        if self.highlighter:
            self.highlighter.setParent(None)

        if highlighterclass:
            self.highlighter = highlighterclass(self.edit.document())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LNTextEdit()
    win.show()

    sys.exit(app.exec_())