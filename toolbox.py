from qss import style
from view.MainWindow import MainWindow
import logging.config

if __name__ == "__main__":
    """
    在PyQt5中,如果在Python 代码中抛出了异常,没有进行捕获,异常只要进入事件循环,程序就崩溃,而没有任何提示,给程序调试带来不少麻烦,通过在程序运行前加入以下代码,则能避免程序崩溃.
    import cgitb 
    cgitb.enable( format = ‘text’)
    """
    import sys
    import qdarkstyle
    import cgitb
    from quamash import QEventLoop, QApplication
    import asyncio

    #修改logging.config源码以utf-8读取文件
    logging.config.fileConfig("logger/logging.conf")
    # 输出日志到控制台和文件,获取的是root对应的logger
    #logger = logging.getLogger()

    # import os
    # curPath = os.path.abspath(os.path.dirname(__file__))
    # rootPath = curPath[:curPath.rfind("Toolbox") + len("Toolbox")]  # Toolbox，也就是项目的根路径
    # os.chdir(rootPath)

    cgitb.enable(logdir=r'logger/cgitb', format='text')
    app = QApplication(sys.argv)
    style.setScrollBarStyle(app)
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        Form = MainWindow()
        Form.resize(1200, 800)
        #Form.resize(800, 600)
        Form.show()
        loop.run_forever()